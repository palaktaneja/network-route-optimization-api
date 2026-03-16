from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class Node(Base):
    """
    Represents a network node/server in the graph.
    Example: ServerA, ServerB
    """
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Edge(Base):
    """
    Represents a connection between two nodes
    along with the network latency.
    """
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    latency = Column(Float, nullable=False)


class RouteHistory(Base):
    """
    Stores previously queried routes for auditing
    and history lookup.
    """
    __tablename__ = "route_history"

    id = Column(Integer, primary_key=True)

    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)

    total_latency = Column(Float)

    # path stored as comma separated values
    path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)