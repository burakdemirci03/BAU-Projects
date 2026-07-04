import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.infrastructure.messaging.stream import stream_manager

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/stream")
async def message_stream(request: Request):
    async def event_generator():
        queue = await stream_manager.connect()
        try:
            while True:
                if await request.is_disconnected():
                    break
                
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield ":ping-pong\n\n"
                    
        finally:
            stream_manager.disconnect(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")