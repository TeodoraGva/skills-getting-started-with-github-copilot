from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_existing_participant():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
