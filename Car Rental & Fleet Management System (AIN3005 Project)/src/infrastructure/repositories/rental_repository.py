from typing import List, Optional
import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.rental import RentalAgreement, Reservation

class RentalRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.reservation_collection = database["reservations"]
        self.agreement_collection = database["agreements"]

    async def save_reservation(self, reservation: Reservation):
        data = reservation.model_dump(mode='json')
        await self.reservation_collection.replace_one(
            {"reservation_id": reservation.reservation_id},
            data,
            upsert=True
        )

    async def find_overlapping_reservations(self, vehicle_id: str, start: datetime.datetime, end: datetime.datetime) -> List[Reservation]:
        query = {
            "vehicle.vehicle_id": vehicle_id,
            "start_date": {"$lt": end},
            "end_date": {"$gt": start}
        }
        cursor = self.reservation_collection.find(query)
        reservations = []
        async for doc in cursor:
            reservations.append(Reservation(**doc))
        return reservations

    async def save_agreement(self, agreement: RentalAgreement):
        data = agreement.model_dump(mode='json')
        await self.agreement_collection.replace_one(
            {"rental_id": agreement.rental_id},
            data,
            upsert=True
        )

    async def get_agreement_by_id(self, rental_id: str) -> Optional[RentalAgreement]:
        doc = await self.agreement_collection.find_one({"rental_id": rental_id})
        if doc:
            return RentalAgreement(**doc)
        return None