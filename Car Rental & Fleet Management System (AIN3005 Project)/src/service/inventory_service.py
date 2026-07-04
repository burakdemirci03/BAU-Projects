import datetime
from typing import List
from src.infrastructure.repositories.vehicle_repository import VehicleRepository
from src.infrastructure.repositories.rental_repository import RentalRepository
from src.domain.vehicle import Vehicle

class InventoryService:
    def __init__(self, vehicle_repo: VehicleRepository, rental_repo: RentalRepository):
        self.vehicle_repo = vehicle_repo
        self.rental_repo = rental_repo

    async def search_available_vehicles(
        self, 
        vehicle_class: str, 
        location_branch: str, 
        start_date: datetime.datetime, 
        end_date: datetime.datetime
    ) -> List[Vehicle]:
        
        candidates = await self.vehicle_repo.find_available(vehicle_class, location_branch)
        available_vehicles = []

        for vehicle in candidates:
            conflicts = await self.rental_repo.find_overlapping_reservations(
                vehicle.vehicle_id, 
                start_date, 
                end_date
            )
            
            if not conflicts:
                available_vehicles.append(vehicle)

        return available_vehicles