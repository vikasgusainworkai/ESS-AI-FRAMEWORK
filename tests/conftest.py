from collections.abc import Iterator

import pytest

from ess_app.users.store import store


@pytest.fixture(autouse=True)
def reset_user_store() -> Iterator[None]:
    store.clear()
    yield
    store.clear()
