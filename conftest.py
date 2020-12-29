import pytest

from api import API


# pytest looks for fixtures by default in this file

@pytest.fixture
def api():
    return API()


@pytest.fixture
def client(api):
    return api.test_session()
