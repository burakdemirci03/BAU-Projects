import datetime
from src.domain.rental import RentalAgreement, RentalStatus
from src.domain.vehicle import Vehicle, Availability
from src.domain.billing import Invoice, BasePricingPolicy, PenaltyCharge
from src.domain.payment import Payment, PaymentStatus
from src.domain.events import PickupCompleted, InvoicePaid

from src.infrastructure.repositories.rental_repository import RentalRepository
from src.infrastructure.repositories.vehicle_repository import VehicleRepository
from src.infrastructure.repositories.billing_repository import BillingRepository
from src.infrastructure.clock import AbstractClock
from src.infrastructure.messaging.event_bus import EventBus

class RentalService:
    def __init__(
        self, 
        rental_repo: RentalRepository, 
        vehicle_repo: VehicleRepository,
        billing_repo: BillingRepository,
        clock: AbstractClock,
        event_bus: EventBus
    ):
        self.rental_repo = rental_repo
        self.vehicle_repo = vehicle_repo
        self.billing_repo = billing_repo
        self.clock = clock
        self.event_bus = event_bus

    async def pickup_vehicle(self, rental_id: str) -> RentalAgreement:
        agreement = await self.rental_repo.get_agreement_by_id(rental_id)
        if not agreement:
            raise ValueError("Rental agreement does not found.")

        if agreement.status == RentalStatus.ACTIVE:
            return agreement

        agreement.pickup()
        
        vehicle = agreement.vehicle
        vehicle.availability = Availability.Rented
        
        await self.vehicle_repo.save(vehicle)
        await self.rental_repo.save_agreement(agreement)

        event = PickupCompleted(
            rental_id=agreement.rental_id,
            vehicle_plate=agreement.vehicle.brand,
            timestamp=self.clock.now()
        )
        await self.event_bus.publish(event)
        
        return agreement

    async def return_vehicle(self, rental_id: str, current_odometer: float, current_fuel: float) -> Invoice:
        current_time = self.clock.now()

        agreement = await self.rental_repo.get_agreement_by_id(rental_id)
        if not agreement:
            raise ValueError("Rental agreement does not found.")
        
        if agreement.status != RentalStatus.ACTIVE:
             raise ValueError("Rental is not active, cannot return.")

        vehicle = agreement.vehicle

        if current_odometer < vehicle.odometer:
            raise ValueError(f"Odometer rollback detected! Current: {vehicle.odometer}, New: {current_odometer}")
        
        vehicle.odometer = current_odometer
        vehicle.fuel_level = current_fuel 
        vehicle.availability = Availability.Available
        agreement.status = RentalStatus.COMPLETED

        policy = BasePricingPolicy() 
        penalty_calc = PenaltyCharge()

        invoice = Invoice(
            rental_id=agreement.rental_id,
            issue_date=current_time
        )

        charges = policy.calculate_pricing(agreement)
        
        late_fee = penalty_calc.calculate_late_fee(agreement, current_time)
        
        for item in charges:
            invoice.add_charge(item)
        
        if late_fee:
            invoice.add_charge(late_fee)

        await self.vehicle_repo.save(vehicle)
        await self.rental_repo.save_agreement(agreement)
        await self.billing_repo.save_invoice(invoice)

        return invoice

    async def process_payment(self, invoice_id: str, amount: float, method: str) -> Payment:
        invoice = await self.billing_repo.get_invoice_by_id(invoice_id)
        if not invoice:
            raise ValueError("Invoice does not found.")

        payment = Payment(
            invoice_id=invoice_id,
            amount=amount,
            method=method
        )

        try:
            success = True 
            if success:
                payment.mark_completed(self.clock.now())
                
                event = InvoicePaid(invoice_id=invoice_id, amount=amount)
                await self.event_bus.publish(event)
            else:
                payment.mark_failed(self.clock.now())
        except Exception:
             payment.mark_failed(self.clock.now())

        await self.billing_repo.save_payment(payment)
        return payment

async def extend_rental(
    self,
    rental_id: str,
    additional_days: int
) -> RentalAgreement:
    agreement = await self.rental_repo.get_agreement_by_id(rental_id)
    if not agreement:
        raise ValueError("Rental agreement not found.")
    
    if agreement.status != RentalStatus.ACTIVE:
        raise ValueError("Can only extend active rentals.")

    new_end_date = agreement.end_date + datetime.timedelta(days=additional_days)

    conflicting_reservations = await self.rental_repo.find_overlapping_reservations(
        agreement.vehicle.vehicle_id,
        agreement.end_date,
        new_end_date
    )
    
    if conflicting_reservations:
        conflict_dates = [r.start_date.date() for r in conflicting_reservations]
        raise ValueError(
            f"Extension conflicts with reservation(s) starting on: {', '.join(str(d) for d in conflict_dates)}"
        )
    
    agreement.extend_rental(additional_days, conflicting_reservations)
    
    await self.rental_repo.save_agreement(agreement)
    
    return agreement