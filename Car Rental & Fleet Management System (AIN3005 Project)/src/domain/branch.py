from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
import datetime
import uuid

if TYPE_CHECKING:
    from src.domain.rental import RentalAgreement 

class Location(BaseModel):
    location_id: str = Field(default_factory=lambda: f"LOC-{str(uuid.uuid4().int)[:10]}")
    branch: str

    model_config = ConfigDict(from_attributes=True)

class Agent(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"AGN-{str(uuid.uuid4().int)[:10]}")
    name: str
    phone_number: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class Customer(BaseModel):
    customer_id: str = Field(default_factory=lambda: f"CST-{str(uuid.uuid4().int)[:10]}")
    name: str
    phone_number: str
    email: str
    rental_record: List["RentalAgreement"] = [] 

    model_config = ConfigDict(from_attributes=True)

    def add_rental_history(self, rental: "RentalAgreement"):
        self.rental_record.append(rental)

    def is_renting_now(self, current_time: datetime.datetime) -> bool:
        if not self.rental_record:
            return False
        
        last_rental = self.rental_record[-1]
        
        if last_rental.start_date and last_rental.end_date:
            return last_rental.start_date <= current_time <= last_rental.end_date
        
        return False