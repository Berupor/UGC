from fastapi import HTTPException
from fastapi.testclient import TestClient

from functional.config import settings
from ugc_service.src.api.v1.bookmarks import router

client = TestClient(router)


def test_add_bookmark():
    payload = {
        "status": "True",
    }
    response = client.post(
        "/12345",
        json=payload,
        headers={"Authorization": f"Bearer {settings.test_token}"},
    )
    assert response.status_code == 200


def test_get_all_bookmarks():
    response = client.get(
        "/", headers={"Authorization": f"Bearer {settings.test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


def test_delete_bookmark_not_found():
    try:
        client.delete(
            "/63d6619fe783147088229a69",
            headers={"Authorization": f"Bearer {settings.test_token}"},
        )

    except HTTPException as e:
        assert e.status_code == 404

    else:
        raise Exception("Test failed")


def test_delete_bookmark_unauthorized():
    try:
        client.delete(
            "/63d6619fe783147088229a69",
            headers={"Authorization": f"Bearer"},
        )

    except HTTPException as e:
        assert e.status_code == 403

    else:
        raise Exception("Test failed")
