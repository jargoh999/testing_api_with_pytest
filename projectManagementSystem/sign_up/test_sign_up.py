import requests
import pytest
from faker import Faker

faker = Faker()

@pytest.fixture
def base_url():
    return "http://localhost:8080"

def test_sign_up(base_url):
    payload = {
        "email": faker.email(),
        "fullName": faker.name(),
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 201
    assert response.json()["jwt"] != ""

def test_sign_up_invalid_email(base_url):
    payload = {
        "email": "invalid-email",
        "fullName": faker.name(),
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

def test_sign_up_missing_email(base_url):
    payload = {
        "fullName": faker.name(),
        "password": faker.password()
    }
    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

def test_sign_up_missing_password(base_url):
    payload = {
        "email": faker.email(),
        "fullName": faker.name()
    }
    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

def test_sign_up_short_password(base_url):
    payload = {
        "email": faker.email(),
        "fullName": faker.name(),
        "password": "short"
    }

    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

def test_sign_up_existing_email(base_url):
    payload = {
        "email": "existing@email.com",
        "fullName": faker.name(),
        "password": faker.password()
    }
  
    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 409

def test_sign_up_special_characters_name(base_url):
    payload = {
        "email": faker.email(),
        "fullName": "fatoye @yomide#3",
        "password": faker.password()
    }

    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

def test_sign_up_long_email(base_url):
    long_email = "a" * 256 + "@example.com"
    payload = {
        "email": long_email,
        "fullName": faker.name(),
        "password": faker.password()
    }

    response = requests.post(f"{base_url}/auth/sign_up", json=payload)
    assert response.status_code == 400

if __name__ == "__main__":
    pytest.main()
