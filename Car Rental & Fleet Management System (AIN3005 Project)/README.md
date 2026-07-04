# CRFMS - Car Rental & Fleet Maintenance System

## Folder Structure

- `src/domain` - Contains core entities and pure business rules.
- `src/api` - Application entry point.
- `src/api/routers` - HTTP endpoints (REST).
- `src/infrastructure` - Adapters for external systems.
- `src/infrastructure/repositories` - MongoDB data access.
- `src/infrastructure/messaging` - Event bus and reactive stream handlers.
- `src/service` - Business use cases.

## How To Run

### 1. Running the System

Run the following command in the root directory to build and start both the Backend API and MongoDB:

```bash
docker-compose up --build
```

### 2. Adding Example Data

When system is ready and running,
execute the following command in the root directory to create an example data on MongoDB:

```bash
python add_example_data.py
```

### 3. Accessing Server

- System can be accessed by following URL:
  http://localhost:8000

- API documentation can be viewed on:
  http://localhost:8000/docs

- Notification system can be accessible with:
  http://localhost:8000/notifications/stream
