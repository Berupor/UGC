from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
import pytest
from api.v1.rating import router
from functional.config import settings
from services.base_service import EventService
from services.rating_service import RatingService
from .utils.mocks import MockEventService, MockMongoService

Client = TestClient(router)


class TestRating:

    def test_add_rating(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(EventService, "produce", MockEventService.mock_produce)

        response = Client.post("/123", json={"text": "True"},
                               headers={"Authorization": f"Bearer {settings.test_token}"}, )

        assert response.json() == 201

    def test_get_ratings(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(RatingService, '__init__', MockMongoService.__init__)
        monkeypatch.setattr(RatingService, 'find', MockMongoService.find)
        response = Client.get(
            "/123", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(isinstance(item, dict) for item in data)

    def test_delete_rating(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(RatingService, '__init__', MockMongoService.__init__)
        monkeypatch.setattr(RatingService, 'delete_one', MockMongoService.delete_one)

        response = Client.delete(
            "/123", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.json() == HTTPStatus.NO_CONTENT
