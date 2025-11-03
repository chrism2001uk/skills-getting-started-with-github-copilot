from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Chess Club"
    
    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    
    # Test nonexistent activity
    response = client.post("/activities/NonexistentClub/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity():
    # First sign up a test user
    email = "unregister_test@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Test successful unregister
    response = client.post("/activities/Chess Club/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    
    # Test unregister from nonexistent activity
    response = client.post("/activities/NonexistentClub/unregister", params={"email": email})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
    # Test unregister user not in activity
    response = client.post("/activities/Chess Club/unregister", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
    
    # Test unregister without email parameter
    response = client.post("/activities/Chess Club/unregister")
    assert response.status_code == 400
    assert "required" in response.json()["detail"]