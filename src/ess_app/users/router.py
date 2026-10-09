from typing import Annotated

from fastapi import APIRouter, Query, Response

from ess_app.users.models import Role, Status, User, UserCreate, UserUpdate
from ess_app.users.store import store

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", status_code=201)
def create_user(data: UserCreate) -> User:
    return store.create(data)


@router.get("")
def list_users(
    q: Annotated[str | None, Query(max_length=100)] = None,
    role: Role | None = None,
    status: Status | None = None,
) -> list[User]:
    return store.search(query=q, role=role, status=status)


@router.get("/{user_id}")
def get_user(user_id: str) -> User:
    return store.get(user_id)


@router.patch("/{user_id}")
def update_user(user_id: str, data: UserUpdate) -> User:
    return store.update(user_id, data)


@router.post("/{user_id}/deactivate")
def deactivate_user(user_id: str) -> User:
    return store.deactivate(user_id)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str) -> Response:
    store.delete(user_id)
    return Response(status_code=204)
