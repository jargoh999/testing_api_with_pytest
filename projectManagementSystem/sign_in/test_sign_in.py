import requests
import pytest
from faker import Faker

faker = Faker()

@pytest.fixture
def base_url():
    return "http://localhost:8080"

def test_sign_in_success(base_url):
    payload = {
      "email": "test@email1",
      "password": "password"  
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 200
    assert "jwt" in response.json()

def test_sign_in_invalid_email(base_url):
    payload = {
        "email": "invalid-email",
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 401

def test_sign_in_missing_email(base_url):
    payload = {
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_missing_password(base_url):
    payload = {
        "email": faker.email()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_incorrect_password(base_url):
    payload = {
        "email": faker.email(),
        "password": "wrongpassword"
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 401

def test_sign_in_short_password(base_url):
    payload = {
        "email": faker.email(),
        "password": "short"
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_long_email(base_url):
    long_email = "a" * 256 + "@example.com"
    payload = {
        "email": long_email,
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_special_characters_email(base_url):
    payload = {
        "email": "test!email12@example.com",
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_spaces_in_email(base_url):
    payload = {
        "email": "test email12@example.com",
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_empty_payload(base_url):
    payload = {}
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_null_email(base_url):
    payload = {
        "email": None,
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_null_password(base_url):
    payload = {
        "email": faker.email(),
        "password": None
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_invalid_json_format(base_url):
    payload = "{email: 'test@email12', password: 'passwordd'}"  # Invalid JSON format
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{base_url}/auth/sign_in", data=payload, headers=headers)
    assert response.status_code == 400

def test_sign_in_excessively_long_password(base_url):
    payload = {
        "email": faker.email(),
        "password": "a" * 256
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload)
    assert response.status_code == 400

def test_sign_in_json_content_type(base_url):
    payload = {
        "email": faker.email(),
        "password": faker.password()
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{base_url}/auth/sign_in", json=payload, headers=headers)
    assert response.status_code == 200
    assert "token" in response.json()
