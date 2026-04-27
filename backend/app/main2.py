from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()

async def root1(request):
    return {"message": "Slotify Backend is running!"}

route = APIRoute(path="/", endpoint=root1, methods=["GET"])
app.router.routes.append(route)