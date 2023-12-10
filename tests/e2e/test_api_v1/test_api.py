from . import api_client


def assert_default_format(response):
    assert "status_code" in response
    assert "success" in response
    assert "message" in response
    assert "data" in response

    assert isinstance(response["status_code"], int)
    assert isinstance(response["success"], bool)
    assert isinstance(response["message"], str)
    assert isinstance(response["data"], dict)


def test_create_user():
    response = api_client.post_create_user(
        username="",
        email="",
        password="",
    )
    assert_default_format(response)

    assert response["status_code"] == 400
    assert response["success"] is False

    response = api_client.post_create_user(
        username="testuser",
        email="",
        password="",
    )
    assert_default_format(response)

    assert response["status_code"] == 400
    assert response["success"] is False

    response = api_client.post_create_user(
        username="testuser",
        email="",  # invalid email
        password="",
    )
    assert_default_format(response)


def test_login():
    response = _extracted_from_test_login_2("", "")
    response = _extracted_from_test_login_2("testuser", "")
    response = _extracted_from_test_login_2("testuser", "testpassword")


# TODO Rename this here and in `test_login`
def _extracted_from_test_login_2(username, password):
    result = api_client.post_login(username=username, password=password)
    assert_default_format(result)

    assert result["status_code"] == 400
    assert result["success"] is False

    return result
