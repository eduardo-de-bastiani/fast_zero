import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


# DRY (don't repeat yourself)
@pytest.fixture
def client():
    return TestClient(app)
