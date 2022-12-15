from fastapi import FastAPI
from .routers import binance, external

app = FastAPI()
app.include_router(binance.router)
app.include_router(external.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}