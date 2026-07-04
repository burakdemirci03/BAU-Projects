from enum import Enum
import uuid
from pydantic import BaseModel, Field

class InsuranceTier(float, Enum):
    NoInsurance = 0.0
    HalfInsurance = 0.5
    FullInsurance = 1.0

class AddOn(BaseModel):
    addon_id: str = Field(default_factory=lambda: f"AON-{str(uuid.uuid4().int)[:10]}")
    name: str
    price: float