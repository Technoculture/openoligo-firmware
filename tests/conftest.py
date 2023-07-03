import pytest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="function", autouse=False)
def db(request):
    initializer(["openoligo.api.models"], "sqlite://:memory:", app_label="models")
    request.addfinalizer(finalizer)
