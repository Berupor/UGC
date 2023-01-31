from fastapi import HTTPException
from fastapi.testclient import TestClient

from ugc_service.tests.functional.config import settings
from ugc_service.src.api.v1.review import router

client = TestClient(router)


def test_add_review():
    response = client.post(
        "/123",
        json={"text": "Test review"},
        headers={"Authorization": f"Bearer {settings.test_token}"},
    )
    assert response.status_code == 200


def test_get_all_reviews():
    response = client.get("/123")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_review_not_found():
    try:
        client.delete(
            "/63d6619fe783147088229a69",
            headers={"Authorization": f"Bearer {settings.test_token}"},
        )

    except HTTPException as e:
        assert e.status_code == 404

    else:
        raise Exception("Test failed")


def test_delete_review_unauthorized():
    try:
        client.delete(
            "/63d6619fe783147088229a69",
            headers={"Authorization": f"Bearer"},
        )

    except HTTPException as e:
        assert e.status_code == 403

    else:
        raise Exception("Test failed")
