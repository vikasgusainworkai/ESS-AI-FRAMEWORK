from threading import Lock
from uuid import uuid4

from ess_app.users.models import Role, Status, User, UserCreate, UserUpdate


class UserNotFoundError(Exception):
    pass


class DuplicateEmailError(Exception):
    pass


class UserStore:
    """In-memory user storage (ADR-001): single process, lost on restart."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._lock = Lock()

    def _ensure_email_free(self, email: str, exclude_id: str | None = None) -> None:
        key = email.casefold()
        if any(u.email.casefold() == key and u.id != exclude_id for u in self._users.values()):
            raise DuplicateEmailError(email)

    def _require(self, user_id: str) -> User:
        try:
            return self._users[user_id]
        except KeyError:
            raise UserNotFoundError(user_id) from None

    def create(self, data: UserCreate) -> User:
        with self._lock:
            self._ensure_email_free(data.email)
            user = User(id=str(uuid4()), **data.model_dump())
            self._users[user.id] = user
            return user

    def search(
        self, query: str | None = None, role: Role | None = None, status: Status | None = None
    ) -> list[User]:
        text = (query or "").strip().casefold()
        with self._lock:
            return [
                u
                for u in self._users.values()
                if (not text or text in u.name.casefold() or text in u.email.casefold())
                and (role is None or u.role is role)
                and (status is None or u.status is status)
            ]

    def get(self, user_id: str) -> User:
        with self._lock:
            return self._require(user_id)

    def update(self, user_id: str, data: UserUpdate) -> User:
        with self._lock:
            user = self._require(user_id)
            changes = data.model_dump(exclude_unset=True)
            if "email" in changes:
                self._ensure_email_free(changes["email"], exclude_id=user_id)
            user = user.model_copy(update=changes)
            self._users[user_id] = user
            return user

    def deactivate(self, user_id: str) -> User:
        return self.update(user_id, UserUpdate(status=Status.INACTIVE))

    def delete(self, user_id: str) -> None:
        with self._lock:
            self._require(user_id)
            del self._users[user_id]

    def clear(self) -> None:
        with self._lock:
            self._users.clear()


store = UserStore()
