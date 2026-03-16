from pydantic import BaseModel, Field
from typing import List


class NodeCreate(BaseModel):
    name: str = Field(..., example="ServerA")


class NodeResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class EdgeCreate(BaseModel):
    source: str = Field(..., example="ServerA")
    destination: str = Field(..., example="ServerB")
    latency: float = Field(..., gt=0, example=12.5)


class EdgeResponse(BaseModel):
    id: int
    source: str
    destination: str
    latency: float

    class Config:
        orm_mode = True


class RouteRequest(BaseModel):
    source: str = Field(..., example="ServerA")
    destination: str = Field(..., example="ServerD")


class RouteResponse(BaseModel):
    total_latency: float
    path: List[str]
    