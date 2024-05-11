import os
from typing import Any, List
from fastapi.routing import APIRouter

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from bson.raw_bson import RawBSONDocument
from bson import encode
from loguru import logger


router = APIRouter()

client = AsyncIOMotorClient(os.environ["MONGON_URL"], server_api=ServerApi("1"))


class TraceRequest(BaseModel):
    post: List[dict[str, Any]] = None
    patch: List[dict[str, Any]] = None


@router.post("/runs/batch")
async def batch(request: TraceRequest):
    col = client.get_database("langchain").get_collection("traces")
    if request.post:
        insert_result = await col.insert_many(
            documents=[RawBSONDocument(encode(item)) for item in request.post]
        )
        logger.info(
            f"插入数量{len(insert_result.inserted_ids)},状态{insert_result.acknowledged}"
        )
    if request.patch:
        for item in request.patch:
            replace_result = await col.replace_one(
                {"id": item["id"]}, RawBSONDocument(encode(item))
            )
            logger.info(
                f"匹配数量{replace_result.matched_count},更新数量{replace_result.modified_count},状态{replace_result.acknowledged}"
            )
    return {"insert": len(insert_result.inserted_ids), "update": 0}
