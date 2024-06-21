# levantar el servidor uvicorn main:app --reload

from fastapi import FastAPI
from routers import patients, appointments

app = FastAPI()

# Routers
app.include_router(patients.router)
app.include_router(appointments.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
