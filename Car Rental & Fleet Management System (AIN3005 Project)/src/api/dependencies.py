from fastapi import Depends
from src.infrastructure.database import get_database
from src.infrastructure.clock import SystemClock, AbstractClock
from src.infrastructure.repositories.vehicle_repository import VehicleRepository
from src.infrastructure.repositories.rental_repository import RentalRepository
from src.infrastructure.repositories.billing_repository import BillingRepository
from src.service.rental_service import RentalService
from src.service.inventory_service import InventoryService
from src.infrastructure.messaging.event_bus import EventBus
from src.infrastructure.messaging.handlers import handle_pickup_notification, handle_invoice_paid_notification
from src.domain.events import PickupCompleted, InvoicePaid

def get_clock() -> AbstractClock:
    return SystemClock()

event_bus_instance = EventBus()
event_bus_instance.subscribe(PickupCompleted, handle_pickup_notification)
event_bus_instance.subscribe(InvoicePaid, handle_invoice_paid_notification)

def get_event_bus() -> EventBus:
    return event_bus_instance

def get_vehicle_repo(db=Depends(get_database)):
    return VehicleRepository(db)

def get_rental_repo(db=Depends(get_database)):
    return RentalRepository(db)

def get_billing_repo(db=Depends(get_database)):
    return BillingRepository(db)

def get_rental_service(
    rental_repo=Depends(get_rental_repo),
    vehicle_repo=Depends(get_vehicle_repo),
    billing_repo=Depends(get_billing_repo),
    clock=Depends(get_clock),
    event_bus=Depends(get_event_bus)
) -> RentalService:
    return RentalService(rental_repo, vehicle_repo, billing_repo, clock, event_bus)

def get_inventory_service(
    vehicle_repo=Depends(get_vehicle_repo),
    rental_repo=Depends(get_rental_repo)
) -> InventoryService:
    return InventoryService(vehicle_repo, rental_repo)