from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from functional.config import settings
from pytest import MonkeyPatch

from api.v1.review import router
from services.base_service import EventService
from services.review_service import ReviewService

from .utils.mocks import MockEventService, MockMongoService

Client = TestClient(router)


class TestReview:
    def test_add_review(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(EventService, "produce", MockEventService.mock_produce)

        response = Client.post(
            "/123",
            json={"text": "True"},
            headers={"Authorization": f"Bearer {settings.test_token}"},
        )

        assert response.json() == 201

    def test_get_all_reviews(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(ReviewService, "__init__", MockMongoService.__init__)
        monkeypatch.setattr(ReviewService, "find", MockMongoService.find)
        response = Client.get(
            "/123", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(isinstance(item, dict) for item in data)

    def test_delete_review(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(ReviewService, "__init__", MockMongoService.__init__)
        monkeypatch.setattr(ReviewService, "delete_one", MockMongoService.delete_one)

        response = Client.delete(
            "/123", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.json() == HTTPStatus.NO_CONTENT
