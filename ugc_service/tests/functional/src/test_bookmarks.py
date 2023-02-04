from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
import pytest
from api.v1.bookmarks import router
from functional.config import settings
from services.base_service import EventService
from services.bookmarks_service import BookmarksService
from .utils.mocks import MockEventService, MockMongoService

Client = TestClient(router)


class TestBookmarks:

    def test_add_bookmark(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(EventService, "produce", MockEventService.mock_produce)

        response = Client.post("/123", json={"status": "True"},
                               headers={"Authorization": f"Bearer {settings.test_token}"}, )

        assert response.json() == 201

    def test_get_all_bookmarks(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(BookmarksService, '__init__', MockMongoService.__init__)
        monkeypatch.setattr(BookmarksService, 'find', MockMongoService.find)
        response = Client.get(
            "/", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(isinstance(item, dict) for item in data)

    def test_delete_movie_bookmark(self, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(BookmarksService, '__init__', MockMongoService.__init__)
        monkeypatch.setattr(BookmarksService, 'delete_one', MockMongoService.delete_one)

        response = Client.delete(
            "/123", headers={"Authorization": f"Bearer {settings.test_token}"}
        )
        assert response.json() == HTTPStatus.NO_CONTENT
