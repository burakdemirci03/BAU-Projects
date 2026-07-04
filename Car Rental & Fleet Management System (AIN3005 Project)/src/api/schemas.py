from pydantic import BaseModel
from datetime import datetime

class ReturnRequest(BaseModel):
    current_odometer: float
    current_fuel: float

class SearchRequest(BaseModel):
    vehicle_class: str
    location_branch: str
    start_date: datetime
    end_date: datetime

class PaymentRequest(BaseModel):
    amount: float
    method: str

class ExtendRentalRequest(BaseModel):
    additional_days: int