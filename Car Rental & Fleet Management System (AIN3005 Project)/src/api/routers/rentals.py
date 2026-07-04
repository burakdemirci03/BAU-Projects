from fastapi import APIRouter, Depends, HTTPException
from src.service.rental_service import RentalService
from src.api.dependencies import get_rental_service
from src.api.schemas import ReturnRequest, PaymentRequest

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/pickup/{rental_id}")
async def pickup_vehicle(
    rental_id: str,
    service: RentalService = Depends(get_rental_service)
):
    try:
        result = await service.pickup_vehicle(rental_id)
        return {"status": "success", "rental_status": result.status, "message": "Vehicle is picked up."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/return/{rental_id}")
async def return_vehicle(
    rental_id: str,
    request: ReturnRequest,
    service: RentalService = Depends(get_rental_service)
):
    try:
        invoice = await service.return_vehicle(
            rental_id, 
            request.current_odometer, 
            request.current_fuel
        )
        return {"status": "success", "invoice_id": invoice.invoice_id, "total": invoice.total_amount}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/pay/{invoice_id}")
async def pay_invoice(
    invoice_id: str,
    request: PaymentRequest,
    service: RentalService = Depends(get_rental_service)
):
    try:
        payment = await service.process_payment(invoice_id, request.amount, request.method)
        return {"status": payment.status, "payment_id": payment.payment_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/extend/{rental_id}")
async def extend_rental(
    rental_id: str,
    additional_days: int,
    service: RentalService = Depends(get_rental_service)
):
    try:
        if additional_days <= 0:
            raise HTTPException(status_code=400, detail="Additional days must be positive")
        
        agreement = await service.extend_rental(rental_id, additional_days)
        return {
            "status": "success",
            "rental_id": agreement.rental_id,
            "new_end_date": agreement.end_date.isoformat(),
            "message": f"Rental extended by {additional_days} day(s)"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))