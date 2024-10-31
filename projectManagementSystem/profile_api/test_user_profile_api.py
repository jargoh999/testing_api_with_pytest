import pytest
import requests

BASE_URL = "http://localhost:8080/api"

@pytest.fixture
def headers():
    return {
        'Accept': '*/*',
        'Host': 'localhost:8080',
        'Connection': 'keep-alive'
    }

@pytest.fixture
def auth_token():
    return 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MzAzNjE0ODUsImV4cCI6MTczMTIyNTQ4NSwiZW1haWwiOiJ0ZXN0QGVtYWlsMSJ9.VmaDjLqPWOVNxqpaRQGmoIJTZlBvUw5I4VLBvSwtVCFiDDDL0VktsrWdFSkJh_k9ia175qnRIazHtRs73rcKMQ'

def test_valid_authorization_token(headers, auth_token):
    headers['Authorization'] = auth_token
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200

def test_missing_authorization_token(headers):
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 401

def test_expired_authorization_token(headers):
    headers['Authorization'] = 'Bearer expired_token'
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 401

def test_invalid_authorization_token(headers):
    headers['Authorization'] = 'Bearer invalid_token'
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 401

def test_missing_header_fields(auth_token):
    headers = {}
    headers['Authorization'] = auth_token
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code != 200 

def test_invalid_endpoint_url(headers, auth_token):
    headers['Authorization'] = auth_token
    response = requests.get(f"{BASE_URL}/invalid_endpoint", headers=headers)
    assert response.status_code == 404

def test_valid_payload_with_additional_fields(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = {'additional_field': 'test'}
    response = requests.get(f"{BASE_URL}/profile", headers=headers, data=payload)
    assert response.status_code == 200

def test_invalid_http_method(headers, auth_token):
    headers['Authorization'] = auth_token
    response = requests.post(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 405

def test_valid_authorization_token_incorrect_profile_data(headers, auth_token):
    headers['Authorization'] = auth_token
    response = requests.get(f"{BASE_URL}/profile/nonexistent", headers=headers)
    assert response.status_code == 404

def test_large_payload(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = {'data': 'x' * 1000000}  # Large payload
    response = requests.get(f"{BASE_URL}/profile", headers=headers, data=payload)
    assert response.status_code == 413

if __name__ == "__main__":
    pytest.main()
