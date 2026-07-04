from src.domain.events import PickupCompleted, InvoicePaid
from src.infrastructure.messaging.stream import stream_manager

async def handle_pickup_notification(event: PickupCompleted):
    msg = f"Vehicle is picked up! (ID: {event.rental_id})"
    print(msg)
    
    await stream_manager.broadcast(msg)

async def handle_invoice_paid_notification(event: InvoicePaid):
    msg = f"Payment is taken! ID: {event.invoice_id} - Billing: ${event.amount}"
    print(msg)
    
    await stream_manager.broadcast(msg)