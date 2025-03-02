from motor.motor_asyncio import AsyncIOMotorDatabase


class OntologiesRepo:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def get_count(self, collection_name: str) -> int:
        collection = self.db.get_collection(collection_name)
        return await collection.count_documents({})

    async def get_by_id(self, collection_name: str, id: str) -> dict:
        collection = self.db.get_collection(collection_name)
        result = await collection.find_one({"_id": id})
        if result is None:
            raise ValueError(f"No document found with id {id}")
        return result
