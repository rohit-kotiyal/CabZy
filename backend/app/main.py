from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.ride import router as ride_router

app = FastAPI(title="CabZy API")

app.include_router(auth_router)
app.include_router(ride_router)

@app.get("/")
def health():
    return {"message": "API is working"}