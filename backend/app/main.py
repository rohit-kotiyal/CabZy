from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.ride import router as ride_router
from app.routes.driver import router as driver_router
from app.routes.admin import router as admin_router


app = FastAPI(title="CabZy API")

app.include_router(auth_router)
app.include_router(ride_router)
app.include_router(driver_router)
app.include_router(admin_router)



@app.get("/")
def health():
    return {"message": "API is working"}