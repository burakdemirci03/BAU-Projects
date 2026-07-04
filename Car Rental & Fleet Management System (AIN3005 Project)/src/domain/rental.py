from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
import datetime
import uuid
from enum import Enum
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.branch import Customer, Agent
    from src.domain.vehicle import Vehicle
    from src.domain.addon import AddOn, InsuranceTier

class RentalStatus(str, Enum):
    PENDING = "PendingPickup"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Reservation(BaseModel):
    reservation_id: str = Field(default_factory=lambda: f"RSV-{str(uuid.uuid4().int)[:10]}")
    customer: Customer
    vehicle: Vehicle
    agent: Agent
    start_date: datetime.datetime
    end_date: datetime.datetime

    def overlaps_with(self, start: datetime.datetime, end: datetime.datetime) -> bool:
        return self.start_date < end and self.end_date > start

class RentalAgreement(BaseModel):
    rental_id: str = Field(default_factory=lambda: f"RNT-{str(uuid.uuid4().int)[:10]}")
    customer: Customer
    vehicle: Vehicle
    agent: Agent
    add_ons: List[AddOn] = Field(default_factory=list)
    insurance: InsuranceTier
    start_date: datetime.datetime
    end_date: datetime.datetime
    status: RentalStatus = RentalStatus.PENDING

    def pickup(self) -> None:
        from src.domain.vehicle import Availability

        if self.vehicle.availability == Availability.Rented:
            if self.status == RentalStatus.ACTIVE:
                return
            raise ValueError("Vehicle is already rented.")
        
        self.vehicle.availability = Availability.Rented
        self.status = RentalStatus.ACTIVE
                
    def extend_rental(self, additional_days: int, existing_reservations: List[Reservation] = None) -> None:
        if additional_days <= 0:
            raise ValueError("Additional days must be a positive integer.")
        
        new_end_date = self.end_date + datetime.timedelta(days=additional_days)
        
        if existing_reservations:
            for reservation in existing_reservations:
                if reservation.start_date <= new_end_date and reservation.vehicle.vehicle_id == self.vehicle.vehicle_id:
                     raise ValueError(f"Extension overlaps with reservation starting on {reservation.start_date.date()}")

        self.end_date = new_end_date