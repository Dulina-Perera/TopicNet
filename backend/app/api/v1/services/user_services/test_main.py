import pytest
from fastapi.testclient import TestClient
from . import models,schemes
from sqlalchemy.orm import Session
from .main import app
from .database import SessionLocal, engine, get_db
from .routers import auth,users
from .utils import hash

client = TestClient(app)

# Mock database setup
def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture to initialize the test user in the database
@pytest.fixture
def setup_test_user():
    db: Session = next(get_test_db())
    test_user = models.User(username="testuser", password=hash("prehashedpassword"))
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    return test_user

def teardown_function():
    db: Session = next(get_test_db())
    
    test_user = users.get_user_by_username(db, "testuser")
    
    if test_user:
        db.delete(test_user)
        db.commit()

# Test for Signing up with same username
def test_register_with_same_username(setup_test_user):
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "prehashedpassword"}, 
    )
    assert response.status_code == 400

# Test for Signing up with different username(teardown function have removed the test_user)
def test_register_with_diff_username():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "prehashedpassword"}, 
    )
    assert response.status_code == 200
    

# Test for login endpoint                                                                       
def test_login_for_access_token(setup_test_user):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "prehashedpassword"},  # Ensure hashed password logic
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Test for verifying token endpoint
def test_verify_token_endpoint(setup_test_user):
    # First, create a valid token using the test user
    access_token = auth.create_access_token(data={"sub": setup_test_user.username})
    
    # Verify token using the endpoint
    response = client.get(f"/verify-token/{access_token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Token is valid"

# Test for invalid token verification
def test_verify_invalid_token():
    invalid_token = "this_is_a_fake_token"
    response = client.get(f"/verify-token/{invalid_token}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Token is invalid or expired"

# Test for uploading feature and storing data
def test_upload_pdfs(setup_test_user):
    content = None
    with open(r"app\test.pdf", "rb") as f:
        response = client.post(
            fr"/uploadfile/{setup_test_user.username}",
            files={"file":f}
        )
    
    
    assert response.status_code == 200