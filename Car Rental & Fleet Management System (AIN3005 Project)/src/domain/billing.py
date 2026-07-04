from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING
import datetime
import math
import uuid
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.rental import RentalAgreement

class ChargeItem(BaseModel):
    description: str
    amount: float

class PricingPolicy(ABC):
    def __init__(self, daily_insurance_cost: float = 25.0, tax_rate: float = 0.16):
        self.daily_insurance_cost = daily_insurance_cost
        self.tax_rate = tax_rate

    @abstractmethod
    def calculate_pricing(self, rental: "RentalAgreement") -> List[ChargeItem]:
        pass

    def total(self, items: List[ChargeItem]) -> float:
        return math.ceil(sum((item.amount for item in items), 0.0))

class BasePricingPolicy(PricingPolicy):
    def calculate_pricing(self, rental: "RentalAgreement") -> List[ChargeItem]:
        charges = []
        days = ((rental.end_date - rental.start_date) + datetime.timedelta(seconds=1)).days + 1
        daily_vehicle_price = rental.vehicle.base_price
        insurance_rate = rental.insurance.value

        if days <= 7:
            discount_rate = 0.0
        elif 7 < days <= 30:
            discount_rate = 0.05
        else:
            discount_rate = 0.15

        total_vehicle_charge = daily_vehicle_price * days * (1.0 - discount_rate)
        charges.append(ChargeItem(description=f"Daily Rental - ({days} days x {daily_vehicle_price * (1.0 - discount_rate)}$)", amount=total_vehicle_charge))

        total_insurance_charge = self.daily_insurance_cost * insurance_rate * days
        charges.append(ChargeItem(description=f"Insurance ({rental.insurance.name})", amount=total_insurance_charge))

        for addon in rental.add_ons:
            charges.append(ChargeItem(description=f"Add-on - ({addon.name})", amount=addon.price))

        total_charge = self.total(charges)
        tax_amount = total_charge * self.tax_rate
        charges.append(ChargeItem(description=f"Tax (%{self.tax_rate * 100})", amount=tax_amount))

        return charges

class SeasonalPricingPolicy(PricingPolicy):
    def calculate_pricing(self, rental: "RentalAgreement") -> List[ChargeItem]:
        charges = []
        holiday_months = (12, 1, 2, 6, 7, 8)
        holiday_multiplier = 1.12

        if rental.start_date.month in holiday_months and rental.end_date.month in holiday_months:
            days = ((rental.end_date - rental.start_date) + datetime.timedelta(seconds=1)).days + 1
            daily_vehicle_price = rental.vehicle.base_price
            insurance_rate = rental.insurance.value

            if days <= 7:
                discount_rate = 0.05
            elif 7 < days <= 30:
                discount_rate = 0.15
            else:
                discount_rate = 0.3
            
            total_vehicle_charge = daily_vehicle_price * days * (1.0 - discount_rate) * holiday_multiplier
            charges.append(ChargeItem(description=f"Daily Rental - ({days} days x {daily_vehicle_price}$)", amount=total_vehicle_charge))

            total_insurance_charge = self.daily_insurance_cost * insurance_rate * days * holiday_multiplier
            charges.append(ChargeItem(description=f"Insurance ({rental.insurance.name})", amount=total_insurance_charge))

            for addon in rental.add_ons:
                charges.append(ChargeItem(description=f"Add-on - ({addon.name})", amount=addon.price))

            total_charge = self.total(charges)
            tax_amount = total_charge * self.tax_rate 
            charges.append(ChargeItem(description=f"Tax (%{self.tax_rate * 100})", amount=tax_amount))

            return charges
        else:
            raise ValueError("Holiday policy can not given for this time period.")

class WeekendPricingPolicy(PricingPolicy):
    def calculate_pricing(self, rental: "RentalAgreement") -> List[ChargeItem]:
        charges = []
        daily_vehicle_price = rental.vehicle.base_price
        insurance_rate = rental.insurance.value

        discount_rate = 0.0
        if rental.start_date.weekday() in (5, 6) and rental.end_date.weekday() in (5, 6):
            discount_rate = 0.1

        total_vehicle_charge = 2 * daily_vehicle_price * (1.0 - discount_rate)
        charges.append(ChargeItem(description=f"Weekend Rental - ({daily_vehicle_price * (1.0 - discount_rate)}$)", amount=total_vehicle_charge))

        total_insurance_charge = 2 * self.daily_insurance_cost * insurance_rate
        charges.append(ChargeItem(description=f"Insurance ({rental.insurance.name})", amount=total_insurance_charge))

        for addon in rental.add_ons:
            charges.append(ChargeItem(description=f"Add-on - ({addon.name})", amount=addon.price))

        total_charge = self.total(charges)
        tax_amount = total_charge * self.tax_rate
        charges.append(ChargeItem(description=f"Tax (%{self.tax_rate * 100})", amount=tax_amount))

        return charges

class PenaltyCharge(BaseModel):
    grace_period: int = 2
    rate_per_day: float = 32.5

    def calculate_late_fee(self, rental: "RentalAgreement", return_date: datetime.datetime) -> Optional[ChargeItem]:
        if return_date < rental.start_date:
            raise ValueError("Return date cannot be before rental start date.")
        
        grace_days = ((return_date - rental.end_date) + datetime.timedelta(seconds=1)).days
        
        if grace_days <= self.grace_period:
            return None
        late_days = grace_days - self.grace_period
        penalty_amount = late_days * self.rate_per_day

        description = f"Late Return Fee ({late_days} Days x ${self.rate_per_day})"
        return ChargeItem(description=description, amount=penalty_amount)

class Invoice(BaseModel):
    invoice_id: str = Field(default_factory=lambda: f"INV-{str(uuid.uuid4().int)[:24]}")
    rental_id: str
    issue_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    total_amount: float = 0.0
    items: List[ChargeItem] = []
    
    def calculate_final_amount(self):
        self.total_amount = sum(item.amount for item in self.items)
        return self.total_amount
    
    def add_charge(self, item: ChargeItem):
        self.items.append(item)
        self.total_amount += item.amount