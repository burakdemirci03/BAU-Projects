from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.vehicle import Vehicle, Availability, MaintenanceRecord

class VehicleRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database["vehicles"]
        self.maintenance_collection = database["maintenances"]

    async def save(self, vehicle: Vehicle):
        data = vehicle.model_dump(mode='json')
        await self.collection.replace_one(
            {"vehicle_id": vehicle.vehicle_id},
            data,
            upsert=True
        )

    async def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        doc = await self.collection.find_one({"vehicle_id": vehicle_id})
        if doc:
            return Vehicle(**doc)
        return None

    async def find_available(self, vehicle_class: str, location_branch: str) -> List[Vehicle]:
        query = {
            "vehicle_class": vehicle_class,
            "availability": Availability.Available.value,
            "location.branch": location_branch
        }
        cursor = self.collection.find(query)
        vehicles = []
        async for doc in cursor:
            vehicles.append(Vehicle(**doc))
        return vehicles

    async def save_maintenance(self, record: MaintenanceRecord):
        data = record.model_dump(mode='json')
        await self.maintenance_collection.replace_one(
            {"record_id": record.record_id},
            data,
            upsert=True
        )