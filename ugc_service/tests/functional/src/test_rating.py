import http

from fastapi import HTTPException
from fastapi.testclient import TestClient

from ugc_service.tests.functional.config import settings
from ugc_service.src.api.v1.rating import router

client = TestClient(router)


def test_add_movie_rating():
    response = client.post(
        "/movie/123",
        json={"rating": 0},
        headers={"Authorization": f"Bearer {settings.test_token}"},
    )
    assert response.json() == http.HTTPStatus.CREATED


def test_get_all_movie_ratings():
    response = client.get("/movie/123")
    assert response.status_code == http.HTTPStatus.OK
    assert isinstance(response.json(), list)


def test_delete_movie_rating_unauthorized():
    try:
        client.delete("/movie/123")
    except HTTPException as e:
        assert e.status_code == 403

    else:
        raise Exception("Test failed")


def test_delete_review_rating_not_found():
    try:
        client.delete(
            "/review/63d7ba598ac5fd3a2bf4a489",
            headers={"Authorization": f"Bearer {settings.test_token}"},
        )
    except HTTPException as e:
        assert e.status_code == 404

    else:
        raise Exception("Test failed")
