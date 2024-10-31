import pytest
import requests
import json

BASE_URL = "http://localhost:8080/api/projects"

# Fixtures for common headers and URL
@pytest.fixture
def headers():
    return {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'localhost:8080',
        'Connection': 'keep-alive'
    }

@pytest.fixture
def auth_token():
    return 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MzAzNjE0ODUsImV4cCI6MTczMTIyNTQ4NSwiZW1haWwiOiJ0ZXN0QGVtYWlsMSJ9.VmaDjLqPWOVNxqpaRQGmoIJTZlBvUw5I4VLBvSwtVCFiDDDL0VktsrWdFSkJh_k9ia175qnRIazHtRs73rcKMQ'

@pytest.fixture
def payload():
    return json.dumps({
        "name": "name",
        "description": "description",
        "tags": ["angular", "node"],
        "category": "full stack project"
    })

# Test Cases
def test_valid_request(headers, auth_token, payload):
    headers['Authorization'] = auth_token
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 200

def test_missing_authorization_token(headers, payload):
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 401

def test_expired_authorization_token(headers, payload):
    headers['Authorization'] = 'Bearer expired_token'
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 401

def test_invalid_authorization_token(headers, payload):
    headers['Authorization'] = 'Bearer invalid_token'
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 401

def test_missing_content_type_header(auth_token):
    headers = {
        'Authorization': auth_token,
        'Accept': '*/*',
        'Host': 'localhost:8080',
        'Connection': 'keep-alive'
    }
    response = requests.post(BASE_URL, headers=headers, data=json.dumps({
        "name": "name",
        "description": "description",
        "tags": ["angular", "node"],
        "category": "full stack project"
    }))
    assert response.status_code == 415

def test_invalid_content_type_header(headers, auth_token, payload):
    headers['Authorization'] = auth_token
    headers['Content-Type'] = 'text/plain'
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 415

def test_missing_required_fields(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "description": "description",
        "tags": ["angular", "node"],
        "category": "full stack project"
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 400

def test_invalid_data_types(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "name": "name",
        "description": "description",
        "tags": "angular, node",
        "category": "full stack project"
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 400

def test_valid_payload_with_extra_fields(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "name": "name",
        "description": "description",
        "tags": ["angular", "node"],
        "category": "full stack project",
        "extra_field": "extra"
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 200

def test_large_payload(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "name": "name",
        "description": "description",
        "tags": ["angular", "node"],
        "category": "full stack project",
        "data": "x" * 1000000
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 413

def test_empty_payload(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({})
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 400

def test_invalid_json_format(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = '{"name": "name", "description": "description", "tags": ["angular", "node"], "category": "full stack project"'
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 400

def test_duplicate_project_name(headers, auth_token, payload):
    headers['Authorization'] = auth_token
    response = requests.post(BASE_URL, headers=headers, data=payload)  # First request
    response = requests.post(BASE_URL, headers=headers, data=payload)  # Duplicate request
    assert response.status_code == 409

def test_valid_request_with_special_characters(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "name": "n@me!",
        "description": "descr!ption",
        "tags": ["angu!ar", "node!"],
        "category": "full stack project!"
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 200

def test_valid_request_with_different_category(headers, auth_token):
    headers['Authorization'] = auth_token
    payload = json.dumps({
        "name": "name",
        "description": "description",
        "tags": ["angular", "node"],
        "category": "backend project"
    })
    response = requests.post(BASE_URL, headers=headers, data=payload)
    assert response.status_code == 200

# Running the test cases
if __name__ == "__main__":
    pytest.main()
