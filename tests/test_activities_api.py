import src.app as app_module


def test_get_activities_returns_activity_details(client):
    # Arrange
    expected_activity = app_module.activities["Chess Club"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["Chess Club"] == expected_activity


def test_new_signup_succeeds(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected_case_insensitively(client):
    # Arrange
    email = "MICHAEL@MERGINGTON.EDU"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_for_unknown_activity_is_rejected(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email(client):
    # Arrange

    # Act
    response = client.post("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422


def test_unregister_succeeds_case_insensitively(client):
    # Arrange
    email = "MICHAEL@MERGINGTON.EDU"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_unknown_student_is_rejected(client):
    # Arrange
    email = "unknown@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up"


def test_unregister_from_unknown_activity_is_rejected(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
