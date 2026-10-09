import pytest
from pydantic import ValidationError

from ess_app.users.models import Role, Status, UserCreate, UserUpdate
from ess_app.users.store import DuplicateEmailError, UserNotFoundError, UserStore


def make(name: str = "Ada Lovelace", email: str = "ada@example.com", **kw: object) -> UserCreate:
    return UserCreate.model_validate({"name": name, "email": email, "role": "user", **kw})


# --- validation ---


def test_create_normalizes_name_and_email() -> None:
    data = make(name="  Ada  ", email="  Ada@Example.COM ")
    assert data.name == "Ada"
    assert data.email == "ada@example.com"
    assert data.status is Status.ACTIVE


@pytest.mark.parametrize("name", ["", "   ", "x" * 101])
def test_invalid_name_rejected(name: str) -> None:
    with pytest.raises(ValidationError):
        make(name=name)


def test_name_at_max_length_accepted() -> None:
    assert len(make(name="x" * 100).name) == 100


@pytest.mark.parametrize(
    "email",
    ["", "plain", "no-at.example.com", "a@b", "a b@example.com", "a@@example.com", "@example.com"],
)
def test_invalid_email_rejected(email: str) -> None:
    with pytest.raises(ValidationError):
        make(email=email)


def test_overlong_email_rejected() -> None:
    with pytest.raises(ValidationError):
        make(email="a" * 250 + "@example.com")


def test_invalid_role_and_status_rejected() -> None:
    with pytest.raises(ValidationError):
        make(role="superuser")
    with pytest.raises(ValidationError):
        make(status="deleted")


def test_unknown_field_rejected() -> None:
    with pytest.raises(ValidationError):
        make(is_admin=True)


def test_update_rejects_explicit_null() -> None:
    with pytest.raises(ValidationError):
        UserUpdate.model_validate({"name": None})


# --- store ---


def test_create_and_get() -> None:
    s = UserStore()
    user = s.create(make())
    assert s.get(user.id) == user
    assert user.role is Role.USER


@pytest.mark.parametrize("dup", ["ada@example.com", "ADA@EXAMPLE.COM", "  Ada@Example.com  "])
def test_duplicate_email_rejected_case_insensitive(dup: str) -> None:
    s = UserStore()
    s.create(make())
    with pytest.raises(DuplicateEmailError):
        s.create(make(name="Other", email=dup))
    assert len(s.search()) == 1


def test_search_by_text_role_and_status() -> None:
    s = UserStore()
    ada = s.create(make())
    grace = s.create(make(name="Grace Hopper", email="grace@navy.mil", role="admin"))
    s.deactivate(grace.id)
    assert s.search(query="HOPPER") == [s.get(grace.id)]
    assert s.search(query="example.com") == [ada]
    assert s.search(role=Role.ADMIN) == [s.get(grace.id)]
    assert s.search(status=Status.ACTIVE) == [ada]
    assert s.search(query="ada", status=Status.INACTIVE) == []
    assert len(s.search()) == 2


def test_update_changes_only_given_fields() -> None:
    s = UserStore()
    user = s.create(make())
    updated = s.update(user.id, UserUpdate(role=Role.MANAGER))
    assert updated.role is Role.MANAGER
    assert updated.name == user.name
    assert updated.email == user.email


def test_update_keeps_own_email_but_rejects_another_users() -> None:
    s = UserStore()
    ada = s.create(make())
    s.create(make(name="Grace", email="grace@example.com"))
    assert s.update(ada.id, UserUpdate(email="ADA@example.com")).email == "ada@example.com"
    with pytest.raises(DuplicateEmailError):
        s.update(ada.id, UserUpdate(email="Grace@Example.com"))
    assert s.get(ada.id).email == "ada@example.com"


def test_deactivate_then_reactivate() -> None:
    s = UserStore()
    user = s.create(make())
    assert s.deactivate(user.id).status is Status.INACTIVE
    assert s.update(user.id, UserUpdate(status=Status.ACTIVE)).status is Status.ACTIVE


def test_delete_removes_user_and_frees_email() -> None:
    s = UserStore()
    user = s.create(make())
    s.delete(user.id)
    with pytest.raises(UserNotFoundError):
        s.get(user.id)
    s.create(make())


@pytest.mark.parametrize("action", ["get", "deactivate", "delete"])
def test_unknown_id_raises_not_found(action: str) -> None:
    with pytest.raises(UserNotFoundError):
        getattr(UserStore(), action)("missing")


def test_update_unknown_id_raises_not_found() -> None:
    with pytest.raises(UserNotFoundError):
        UserStore().update("missing", UserUpdate(name="X"))
