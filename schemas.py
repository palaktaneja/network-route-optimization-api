from pydantic import BaseModel, Field
from typing import List


class NodeCreate(BaseModel):
    """
    Schema used when creating a new node.
    """
    name: str = Field(..., example="ServerA")


class NodeResponse(BaseModel):
    """
    Response schema for node endpoints.
    """
    id: int
    name: str

    class Config:
        orm_mode = True


class EdgeCreate(BaseModel):
    """
    Schema used when creating a connection between nodes.
    """
    source: str = Field(..., example="ServerA")
    destination: str = Field(..., example="ServerB")
    latency: float = Field(..., gt=0, example=12.5)


class EdgeResponse(BaseModel):
    """
    Response schema for edge endpoints.
    """
    id: int
    source: str
    destination: str
    latency: float

    class Config:
        orm_mode = True


class RouteRequest(BaseModel):
    """
    Request schema to compute shortest route.
    """
    source: str = Field(..., example="ServerA")
    destination: str = Field(..., example="ServerD")


class RouteResponse(BaseModel):
    """
    Response returned for shortest path query.
    """
    total_latency: float
    path: List[str]
    