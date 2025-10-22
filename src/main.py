from fastapi import FastAPI
from pacientes.router import router as pacientes_router
from database import init_db

app = FastAPI()
app.include_router(pacientes_router)


@app.on_event("startup")
def on_startup():
    init_db()