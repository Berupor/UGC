# from services.review_service import get_review_service
# import asyncio
# from bson import ObjectId
# from pydantic import BaseModel, Field as PydanticField
#
# service = get_review_service()
#
#
# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")
#
#
# class Review(BaseModel):
#     text: str
#     publication_date: str
#     movie_id: str
#     id: PyObjectId = PydanticField(default_factory=PyObjectId, alias="_id")
#
#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True  # required for the _id
#         json_encoders = {ObjectId: str}
#
#
# async def getting():
#     cursor = service.find({})
#
#     async for review in cursor:
#         print(Review(**review))
#
#
# async def finding():
#     review_id = ObjectId('63ccc0d248c4be94a91eddf9')
#     result = await service.find_one({"author": "Vasya"})
#     print(Review(result))
#
#
# # print(asyncio.run(finding()))
# print(asyncio.run(getting()))
#
# # cursor = service.read({})
# # cursor = service.read({"name":"John"})


# =[=[[=[[[[=[=[=[[[=[=]]]]]]]]]]]]]
from event_streamer.kafka_streamer import get_kafka
import asyncio

stream = get_kafka()


async def get_messages():
    generator = stream.consume_messages("reviews")

    async for message in generator:
        print(message)


asyncio.run(get_messages())
