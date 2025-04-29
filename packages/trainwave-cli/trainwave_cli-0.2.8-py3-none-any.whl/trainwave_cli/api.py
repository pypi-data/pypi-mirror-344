import socket
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from http import HTTPStatus
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp
import httpx
from tqdm import tqdm

from trainwave_cli.utils import from_dict


class JobStatus(Enum):
    SUBMIT_CODE = "SUBMIT_CODE"
    LAUNCHING = "LAUNCHING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    UPLOADING = "UPLOADING"
    SUCCESS = "SUCCESS"
    USER_PROCESS_FAILED = "USER_PROCESS_FAILED"
    SYSTEM_TERMINATED = "SYSTEM_TERMINATED"
    USER_CANCELLED = "USER_CANCELLED"

    @classmethod
    def from_str(cls, provider: str) -> "JobStatus | None":
        if provider.upper() not in JobStatus.__members__:
            return None
        return cls(provider.upper())


@dataclass(frozen=True)
class CloudOffer:
    cpus: int = 0
    memory_mb: int = 0
    compliance_soc2: bool = False
    gpu_type: str | None = None
    gpu_memory_mb: int = 0
    gpus: int = 0


@dataclass
class JobConfig:
    id: str
    rid: str
    name: str
    expires_at: int = -1
    cpus: int = 0
    gpus: int = 0
    gpu_type: str | None = None


@dataclass(frozen=True)
class TrainWaveUser:
    id: str
    rid: str
    email: str
    first_name: str | None = None
    last_name: str | None = None


@dataclass(frozen=True)
class TrainwaveOrganization:
    id: str
    rid: str
    name: str
    computed_credit_balance: int = 0


@dataclass(frozen=True)
class TrainwaveProject:
    id: str
    rid: str
    name: str


@dataclass
class Job:
    id: str
    rid: str
    state: JobStatus
    s3_url: str
    project: TrainwaveProject
    cloud_offer: CloudOffer
    cost_per_hour: float
    config: JobConfig
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    total_cost: int = 0
    upload_url: str = ""
    url: str | None = None


@dataclass(frozen=True)
class Secret:
    id: str
    rid: str
    name: str
    organization: str
    digest: str
    project: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class DjangoPagination:
    count: int
    results: list[dict[str, Any]]
    next: str | None = None
    previous: str | None = None


class CLIAuthStatus(Enum):
    NOT_FOUND = "NOT_FOUND"
    NOT_COMPLETED = "NOT_COMPLETED"
    SUCCESS = "SUCCESS"


class CLIConfigSessionStatus(Enum):
    COMPLETE = "complete"
    PENDING = "pending"


class Api:
    def __init__(
        self,
        api_key: str | None,
        endpoint: str,
        project: str = "",
        organization: str = "",
    ):
        verify_ssl = "trainwave.dev" not in endpoint
        endpoint = endpoint.rstrip("/")
        self.client = httpx.AsyncClient(base_url=endpoint, verify=verify_ssl, timeout=15)
        self.api_key = api_key
        self.project = project
        self.organization = organization

    async def request(self, method, path, **kwargs):
        headers = kwargs.pop("headers", {})
        headers["X-Api-Key"] = self.api_key
        path = f"/{path.lstrip('/')}"
        res = await self.client.request(method, path, headers=headers, **kwargs)
        self._ensure_no_errors(res)
        return res

    def _ensure_no_errors(self, res: httpx.Response) -> httpx.Response:
        if res.status_code >= HTTPStatus.BAD_REQUEST.value:
            raise ValueError(f"Error: {res.text}")
        return res

    async def unauthenticated_request(self, method: str, path: str, **kwargs) -> httpx.Response:
        res = await self.client.request(method, path, **kwargs)
        return self._ensure_no_errors(res)

    async def create_cli_config_session(self, existing_config: dict[str, Any]) -> tuple[str, str]:
        res = await self.request("POST", "/api/v1/cli/config_session/", json=existing_config)
        json_body = res.json()
        return str(json_body["url"]), str(json_body["token"])

    async def check_cli_config_session_status(
        self, token: str
    ) -> tuple[CLIConfigSessionStatus, dict[str, Any] | None]:
        res = await self.request("GET", f"/api/v1/cli/{token}/config/")
        self._ensure_no_errors(res)
        json_body = res.json()
        return CLIConfigSessionStatus(json_body["status"]), json_body.get("config")

    async def create_cli_auth_session(self) -> tuple[str, str]:
        res = await self.unauthenticated_request(
            "POST", "/api/v1/cli/create_session/", json={"name": socket.gethostname()}
        )
        json_body = res.json()
        return str(json_body["url"]), str(json_body["token"])

    async def check_cli_auth_session_status(self, token: str) -> tuple[CLIAuthStatus, str | None]:
        res = await self.unauthenticated_request(
            "POST", f"/api/v1/cli/session_status/", json={"token": token}
        )
        self._ensure_no_errors(res)

        if res.status_code == HTTPStatus.ACCEPTED.value:
            return CLIAuthStatus.NOT_COMPLETED, None

        api_token = res.json().get("api_token")
        return CLIAuthStatus.SUCCESS, api_token

    async def check_api_key(self) -> bool:
        try:
            res = await self.request("GET", "/api/v1/organizations/")
            return res.status_code == HTTPStatus.OK.value and len(res.json()["results"]) > 0
        except ValueError:
            return False

    async def list_organizations(self) -> list[TrainwaveOrganization]:
        res = await self.request("GET", "/api/v1/organizations/")
        res.raise_for_status()
        return [from_dict(TrainwaveOrganization, org) for org in res.json()["results"]]

    async def list_projects(self, organization_id: str) -> list[TrainwaveProject]:
        res = await self.request("GET", "/api/v1/projects/")
        res.raise_for_status()
        return [from_dict(TrainwaveProject, project) for project in res.json()["results"]]

    async def create_project(self, organization_id: str, name: str) -> TrainwaveProject:
        res = await self.request(
            "POST",
            "/api/v1/projects/",
            json={"name": name, "organization": organization_id},
        )
        res.raise_for_status()
        return from_dict(TrainwaveProject, res.json())

    async def get_myself(self) -> TrainWaveUser:
        res = await self.request("GET", "/api/v1/users/me/")
        res.raise_for_status()
        json_body = res.json()
        return TrainWaveUser(
            id=json_body.get("id"),
            rid=json_body.get("rid"),
            first_name=json_body.get("first_name"),
            last_name=json_body.get("last_name"),
            email=json_body.get("email"),
        )

    async def list_jobs(self) -> list[Job]:
        path = f"/api/v1/jobs/?org_id={self.organization}"
        res = await self.request(
            "GET",
            path,
        )
        return [from_dict(Job, job) for job in res.json()["results"]]

    async def create_job(self, config: dict[str, Any]) -> Job:
        res = await self.request(
            "POST",
            "api/v1/jobs/",
            json={
                "project": self.project,
                "config": config,
            },
        )
        return from_dict(Job, res.json())

    async def job_status(self, job_id: str) -> JobStatus | None:
        job = await self.get_job(job_id)
        return job.state

    async def get_job(self, job_id: str) -> Job:
        res = await self.request("GET", f"/api/v1/jobs/{job_id}/")
        return from_dict(Job, res.json())

    async def cancel_job(self, job_id: str) -> None:
        await self.request("POST", f"/api/v1/jobs/{job_id}/cancel/", json={})

    async def list_secrets(self, org_id: str) -> list[Secret]:
        res = await self.request("GET", f"/api/v1/organizations/{org_id}/secrets/")
        res_json = res.json()
        values = res_json.get("results", [])
        return [from_dict(Secret, v) for v in values]

    async def set_secrets(
        self, org_id: str, secrets: dict[str, str], project: str | None = None
    ) -> None:
        data: dict[str, Any] = {"secrets": [{"name": k, "value": v} for k, v in secrets.items()]}
        if project:
            data["project"] = project

        await self.request("POST", f"/api/v1/organizations/{org_id}/secrets/", json=data)

    async def unset_secrets(self, org_id: str, secrets: list[str]) -> None:
        for secret in secrets:
            await self.request("DELETE", f"/api/v1/organizations/{org_id}/secrets/{secret}/")

    async def code_submission(self, job: Job) -> None:
        await self.request("POST", f"/api/v1/jobs/{job.id}/code_submission/")

    async def upload_code(
        self, tarball: Path, presigned_url: str, show_progress_bar: bool = True
    ) -> None:
        size = tarball.stat().st_size

        progress_bar = (
            tqdm(total=size, unit="B", unit_scale=True, desc="Uploading")
            if show_progress_bar
            else None
        )

        async def file_chunk_iterator(filename):
            async with aiofiles.open(filename, "rb") as file:
                while True:
                    chunk = await file.read(64 * 1024)
                    if not chunk:
                        break
                    if show_progress_bar:
                        progress_bar.update(len(chunk))
                    yield chunk

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/gzip", "Content-Length": str(size)}
            response = await session.put(
                presigned_url, headers=headers, data=file_chunk_iterator(tarball)
            )
            response.raise_for_status()
