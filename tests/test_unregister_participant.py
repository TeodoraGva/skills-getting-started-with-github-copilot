from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_existing_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity = activities[activity_name]

    if email not in activity["participants"]:
        activity["participants"].append(email)

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activity["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
