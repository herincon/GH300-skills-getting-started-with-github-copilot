import sys
from pathlib import Path
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    # Arrange
    for activity in app_module.activities.values():
        activity["participants"] = []
    yield
    for activity in app_module.activities.values():
        activity["participants"] = []


def test_unregister_participant_removes_the_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email]
    client = TestClient(app_module.app)

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
