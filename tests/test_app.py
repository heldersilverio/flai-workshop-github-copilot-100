import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "Chess Club" in response.json()

def test_signup_for_activity_success():
    response = client.post("/activities/Art Studio/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Art Studio"

    # Cleanup
    client.delete("/activities/Art Studio/participants/test@mergington.edu")

def test_signup_for_activity_already_signed_up():
    email = "emma@mergington.edu"
    response = client.post("/activities/Programming Class/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant_success():
    # Add participant first
    client.post("/activities/Drama Club/signup", params={"email": "remove@mergington.edu"})
    response = client.delete("/activities/Drama Club/participants/remove@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Removed remove@mergington.edu from Drama Club"

def test_remove_participant_not_found():
    response = client.delete("/activities/Drama Club/participants/notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
