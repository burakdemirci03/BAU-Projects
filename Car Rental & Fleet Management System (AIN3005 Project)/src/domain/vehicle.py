from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
import uuid
import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

if TYPE_CHECKING:
    from src.domain.branch import Location


class Availability(str, Enum):
    Available = "Available"
    Reserved = "Reserved"
    Rented = "Rented"
    OutOfService = "OutOfService"
    InCleaning = "InCleaning"


class Vehicle(BaseModel):
    vehicle_id: str = Field(default_factory=lambda: f"VHC-{str(uuid.uuid4().int)[:10]}")
    brand: str
    vehicle_class: str
    odometer: float = Field(default=0.0, ge=0)
    fuel_level: float = Field(ge=0)
    fuel_tank: float = Field(gt=0)
    fuel_consumption: float = Field(gt=0)
    location: Location
    base_price: float = Field(gt=0)
    availability: Availability = Availability.Available

    
    @model_validator(mode='after')
    def check_fuel_capacity(self):
        if self.fuel_level > self.fuel_tank:
            raise ValueError("Fuel level cannot exceed fuel tank capacity.")
        return self

    def is_assignable(self) -> bool:
        return self.availability == Availability.Available

    def add_fuel(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Fuel amount must be positive.")
        
        new_level = self.fuel_level + amount
        if new_level < self.fuel_tank:
            self.fuel_level = new_level
        else:
            self.fuel_level = self.fuel_tank

    def get_range(self) -> float:
        if self.fuel_consumption <= 0:
            return 0.0
        km_per_liter = 100 / self.fuel_consumption
        return km_per_liter * self.fuel_level


class MaintenanceRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"MNT-{str(uuid.uuid4().int)[:10]}")
    vehicle_id: str
    description: str
    price: float
    date: datetime.datetime