from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.billing import Invoice
from src.domain.payment import Payment, NotificationLog

class BillingRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.invoice_collection = database["invoices"]
        self.payment_collection = database["payments"]
        self.notification_collection = database["notifications"]

    async def save_invoice(self, invoice: Invoice):
        data = invoice.model_dump(mode='json')
        await self.invoice_collection.replace_one(
            {"invoice_id": invoice.invoice_id},
            data,
            upsert=True
        )

    async def get_invoice_by_id(self, invoice_id: str) -> Optional[Invoice]:
        doc = await self.invoice_collection.find_one({"invoice_id": invoice_id})
        if doc:
            return Invoice(**doc)
        return None

    async def save_payment(self, payment: Payment):
        data = payment.model_dump(mode='json')
        await self.payment_collection.replace_one(
            {"payment_id": payment.payment_id},
            data,
            upsert=True
        )
        
    async def save_notification_log(self, log: NotificationLog):
        data = log.model_dump(mode='json')
        await self.notification_collection.insert_one(data)