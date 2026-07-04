from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DomainEvent(BaseModel):
    occurred_at: datetime = datetime.now()

class ReservationConfirmed(DomainEvent):
    reservation_id: str
    customer_email: str

class PickupCompleted(DomainEvent):
    rental_id: str
    vehicle_plate: str 
    timestamp: datetime

class InvoicePaid(DomainEvent):
    invoice_id: str
    amount: float
    customer_email: Optional[str] = None