from fastapi import FastAPI
from database import engine, Base

import models
import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Network Route Optimization API",
    description="API to manage network nodes and calculate shortest routes based on latency",
    version="1.0.0"
)

app.include_router(routes.router)


@app.get("/")
def home():
    return {"message": "Network Route Optimization API is running"}