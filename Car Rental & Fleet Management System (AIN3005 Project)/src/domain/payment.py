from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from enum import Enum
import uuid
import datetime
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.billing import Invoice

class PaymentStatus(str, Enum):
    FAILED = "Failed"
    PENDING = "Pending"
    COMPLETED = "Completed"

class Payment(BaseModel):
    payment_id: str = Field(default_factory=lambda: f"PAY-{str(uuid.uuid4().int)[:10]}")
    invoice_id: str
    amount: float
    method: str
    status: PaymentStatus = PaymentStatus.PENDING
    processed_at: Optional[datetime.datetime] = None

    def mark_completed(self, timestamp: datetime.datetime) -> None:
        self.status = PaymentStatus.COMPLETED
        self.processed_at = timestamp

    def mark_failed(self, timestamp: datetime.datetime) -> None:
        self.status = PaymentStatus.FAILED
        self.processed_at = timestamp

class NotificationLog(BaseModel):
    notification_id: str = Field(default_factory=lambda: f"NOT-{str(uuid.uuid4().int)[:10]}")
    payment_id: str
    customer_id: str
    message: str
    sent_at: datetime.datetime