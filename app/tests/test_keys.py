from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from utils.database import Base
from dependencies import get_db, get_token_header
import datetime


def override_get_token_header():
    return True


app.dependency_overrides[get_token_header] = override_get_token_header

client = TestClient(app)


def test_get_single_cred_404():
    response = client.get("/v1/credentials/c2fa95a2-ee1f-4910-b7be-ae3c81e91508")
    assert response.status_code == 404


def test_create_cred_201():
    response = client.post("/v1/credentials", json={
        "id": "4f07cf23-cd0f-42b5-99c4-efa9022adccf",
        "resource": "4f07cf23-cd0f-42b5-99c4-efa9022adccf",
        "encrypted_key": "Test key",
        "public_key": "Test public key",
        "expire_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active": False
    })
    assert response.status_code == 200


def test_get_single_cred_200():
    response = client.get("/v1/credentials/4f07cf23-cd0f-42b5-99c4-efa9022adccf")
    assert response.status_code == 200


def test_delete_cred_204():
    response = client.delete("/v1/credentials/4f07cf23-cd0f-42b5-99c4-efa9022adccf")
    assert response.status_code == 204
