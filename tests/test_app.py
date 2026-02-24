def test_app_import():
    """
    Basic test: check the Flask app can be imported.
    """
    from app import app
    assert app is not None


def test_home_route_status():
    """
    Smoke test: homepage should respond with 200 or redirect (302).
    """
    from app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code in [200, 302]
