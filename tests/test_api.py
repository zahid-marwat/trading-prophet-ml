from api.main import app


def test_api_app_exists() -> None:
    assert app is not None
