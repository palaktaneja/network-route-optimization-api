from fastapi import FastAPI
from database import engine, Base

import models

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Network Route Optimization API",
    description="API to manage network nodes and calculate shortest routes based on latency",
    version="1.0.0"
)


@app.get("/")
def home():
    """
    Simple health check endpoint.
    """
    return {"message": "Network Route Optimization API is running"}