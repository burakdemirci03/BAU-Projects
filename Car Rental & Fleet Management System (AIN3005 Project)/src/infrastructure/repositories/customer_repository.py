from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.branch import Customer

class CustomerRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database["customers"]

    async def save(self, customer: Customer):
        data = customer.model_dump(mode='json')
        await self.collection.replace_one(
            {"customer_id": customer.customer_id},
            data,
            upsert=True
        )

    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        doc = await self.collection.find_one({"customer_id": customer_id})
        if doc:
            return Customer(**doc)
        return None

    async def get_by_email(self, email: str) -> Optional[Customer]:
        doc = await self.collection.find_one({"email": email})
        if doc:
            return Customer(**doc)
        return None