from fastapi import FastAPI
from pacientes.router import router as pacientes_router
from antropometrias.router import router as antropometria_router
from planos.router import router as plano_router
from database import init_db

app = FastAPI()
app.include_router(pacientes_router)
app.include_router(antropometria_router)
app.include_router(plano_router)


@app.on_event("startup")
def on_startup():
    init_db()