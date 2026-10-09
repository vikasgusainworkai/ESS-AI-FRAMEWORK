import re
from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, StringConstraints, field_validator

EMAIL_MAX_LENGTH = 254
EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


def _normalize_email(value: str) -> str:
    value = value.strip().lower()
    if len(value) > EMAIL_MAX_LENGTH:
        raise ValueError(f"must be at most {EMAIL_MAX_LENGTH} characters")
    if not EMAIL_PATTERN.fullmatch(value):
        raise ValueError("must be a valid email address, like name@example.com")
    return value


Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Email = Annotated[str, AfterValidator(_normalize_email)]


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name
    email: Email
    role: Role
    status: Status = Status.ACTIVE


class UserUpdate(BaseModel):
    """Partial update: only the fields sent are changed."""

    model_config = ConfigDict(extra="forbid")

    name: Name | None = None
    email: Email | None = None
    role: Role | None = None
    status: Status | None = None

    @field_validator("name", "email", "role", "status", mode="before")
    @classmethod
    def _reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("cannot be null; leave the field out to keep its value")
        return value


class User(BaseModel):
    id: str
    name: str
    email: str
    role: Role
    status: Status
