from fastapi import APIRouter, Depends, Query
from datetime import datetime
from src.service.inventory_service import InventoryService
from src.api.dependencies import get_inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/search")
async def search_vehicles(
    vehicle_class: str,
    location: str,
    start_date: datetime,
    end_date: datetime,
    service: InventoryService = Depends(get_inventory_service)
):
    
    results = await service.search_available_vehicles(vehicle_class, location, start_date, end_date)
    return results