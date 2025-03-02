"""
This module contains the OntologiesRepo class, which is responsible for
interacting with the MongoDB database that stores the ontologies.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase


class OntologiesRepo:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def get_count(self, collection_name: str) -> int:
        """Get the count of documents in the specified collection."""
        collection = self.db.get_collection(collection_name)
        return await collection.count_documents({})

    async def get_by_id(self, collection_name: str, id: str) -> dict:
        """Get a document JSON by its ID from the specified collection."""
        collection = self.db.get_collection(collection_name)
        result = await collection.find_one({"_id": id})
        if result is None:
            raise ValueError(f"No document found with id {id}")
        return result
