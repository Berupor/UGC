from services.review_service import get_review_service
import asyncio
from bson.objectid import ObjectId

service = get_review_service()


async def getting():
    cursor = service.find({})

    async for review in cursor:
        print(review)


async def finding():
    review_id = ObjectId('63ccc0d248c4be94a91eddf9')
    result = await service.find_one({"author": "Vasya"})
    print(result)


# print(asyncio.run(finding()))
print(asyncio.run(getting()))

# cursor = service.read({})
# cursor = service.read({"name":"John"})
