from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.ride import router as ride_router
from app.routes.driver import router as driver_router
from app.routes.admin import router as admin_router


app = FastAPI(title="CabZy API")


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(ride_router)
app.include_router(driver_router)
app.include_router(admin_router)



@app.get("/")
def health():
    return {"message": "API is working"}