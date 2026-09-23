from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def isolate_activities():
    original_activities = app_module.activities
    app_module.activities = deepcopy(original_activities)
    yield
    app_module.activities = original_activities
