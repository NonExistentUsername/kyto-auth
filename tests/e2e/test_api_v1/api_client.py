from typing import Dict

from fastapi.testclient import TestClient

from src import config
from src.entrypoints.fastapi_app.app import create_app

_client = TestClient(create_app())


def post_create_user(
    username: str,
    email: str,
    password: str,
) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/register",
        params={
            "username": username,
            "email": email,
            "password": password,
        },
    ).json()


def post_login(
    username: str,
    password: str,
) -> Dict:
    return _client.post(
        f"{config.get_api_url()}/v1/login",
        params={
            "username": username,
            "password": password,
        },
    ).json()
