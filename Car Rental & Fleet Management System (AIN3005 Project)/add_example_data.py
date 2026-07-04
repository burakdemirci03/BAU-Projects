import asyncio
from datetime import datetime, timedelta
from src.infrastructure.database import db
from src.domain.addon import InsuranceTier, AddOn
from src.domain.branch import Location, Customer, Agent
from src.domain.rental import RentalStatus, RentalAgreement
from src.domain.vehicle import Vehicle, Availability

Location.model_rebuild()
Vehicle.model_rebuild()
Customer.model_rebuild()
RentalAgreement.model_rebuild()

async def seed():
    
    db.connect()
    database = db.get_db()

    await database["vehicles"].delete_many({})
    await database["agreements"].delete_many({})
    await database["customers"].delete_many({})
    await database["agents"].delete_many({})
    await database["locations"].delete_many({})


    # Location (İstanbul)
    location = Location(branch="İstanbul")
    
    # Agent (Mustafa Demirci)
    agent = Agent(
        name="Mustafa Demirci",
        phone_number="123-40-555",
        email="mustafa.demirci@examplery.com"
    )

    # Customer (Burak Demirci)
    customer = Customer(
        name="Burak Demirci",
        phone_number="123-45-666",
        email="burak.demirci@examplery.com"
    )

    # Vehicle (Ford Mustang)
    vehicle = Vehicle(
        brand="Ford Mustang",
        vehicle_class="Muscle Car", 
        odometer=37.50,
        fuel_level=45.75,
        fuel_consumption=12.25,
        fuel_tank=60.0,
        location=location,
        base_price=450.0,
        availability=Availability.Available
    )

    # Addons (GPS Navigation)
    gps_addon = AddOn(name="GPS Navigation", price=15.0)

    # Rental Agreement (Reservation)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=5)

    agreement = RentalAgreement(
        customer=customer,
        vehicle=vehicle,
        agent=agent,
        add_ons=[gps_addon],
        insurance=InsuranceTier.FullInsurance,
        start_date=start_date,
        end_date=end_date,
        status=RentalStatus.PENDING
    )

    await database["locations"].insert_one(location.model_dump(mode='json'))
    await database["agents"].insert_one(agent.model_dump(mode='json'))
    await database["customers"].insert_one(customer.model_dump(mode='json'))
    await database["vehicles"].insert_one(vehicle.model_dump(mode='json'))
    await database["agreements"].insert_one(agreement.model_dump(mode='json'))

    print(f"Vehicle: {vehicle.brand} ({vehicle.vehicle_class})")
    print(f"Customer: {customer.name}")
    print(f"Rental ID: {agreement.rental_id}")

    db.close()

if __name__ == "__main__":
    asyncio.run(seed())