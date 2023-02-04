class MockEventService:
    async def mock_produce(self, key, topic_name, data):
        pass


class MockMongoService:
    def __init__(self, db_name, collection_name, client):
        ...

    async def find(self, query, **kwargs):
        result = [{"id": 1, "data": "The Shawshank Redemption"},
                  {"id": 2, "data": "The Godfather"}]

        for item in result:
            yield item

    async def delete_one(self, query):
        return 'Successfully deleted'
