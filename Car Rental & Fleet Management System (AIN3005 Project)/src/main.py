from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infrastructure.database import db
from src.api.routers import rentals, inventory, notifications

from src.domain.addon import InsuranceTier, AddOn
from src.domain.branch import Location, Customer, Agent
from src.domain.rental import RentalStatus, RentalAgreement
from src.domain.vehicle import Vehicle, Availability

Location.model_rebuild()
Vehicle.model_rebuild()
Customer.model_rebuild()
Agent.model_rebuild()
RentalAgreement.model_rebuild()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(
    title="CRFMS Backend API",
    description="Car Rental & Fleet Maintenance System",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(rentals.router)
app.include_router(inventory.router)
app.include_router(notifications.router)

@app.get("/")
def home():
    return {"message": "CRFMS System is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)