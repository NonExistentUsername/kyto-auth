from typing import Dict

from fastapi.testclient import TestClient

from auth import config
from auth.entrypoints.fastapi_app.app import create_app

_client = TestClient(create_app())


def post_create_user(
    username: str,
    email: str,
    password: str,
) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/users",
        params={
            "username": username,
            "email": email,
            "password": password,
        },
    ).json()
