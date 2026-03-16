from fastapi import FastAPI

# creating the API application
app = FastAPI(
    title="Network Route Optimization API",
    description="API to manage network nodes and calculate shortest routes based on latency",
    version="1.0.0"
)


@app.get("/")
def home():
    """
    Basic health check endpoint.
    Useful to confirm the API is running.
    """
    return {"message": "Network Route Optimization API is running"}