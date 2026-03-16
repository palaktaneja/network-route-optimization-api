from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from graph_service import shortest_path
from datetime import datetime
from fastapi import Query

import models
import schemas
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/nodes", response_model=schemas.NodeResponse)
def add_node(node: schemas.NodeCreate, db: Session = Depends(get_db)):

    existing = db.query(models.Node).filter(models.Node.name == node.name).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Node with this name already exists"
        )

    new_node = models.Node(name=node.name)

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node


@router.get("/nodes", response_model=list[schemas.NodeResponse])
def get_nodes(db: Session = Depends(get_db)):
    nodes = db.query(models.Node).all()

    return nodes

@router.post("/edges", response_model=schemas.EdgeResponse)
def add_edge(edge: schemas.EdgeCreate, db: Session = Depends(get_db)):

    if edge.latency <= 0:
        raise HTTPException(
            status_code=400,
            detail="Latency must be greater than 0"
        )

    source_node = db.query(models.Node).filter(
        models.Node.name == edge.source
    ).first()

    destination_node = db.query(models.Node).filter(
        models.Node.name == edge.destination
    ).first()

    if not source_node or not destination_node:
        raise HTTPException(
            status_code=400,
            detail="Source or destination node not found"
        )

    existing_edge = db.query(models.Edge).filter(
        models.Edge.source == edge.source,
        models.Edge.destination == edge.destination
    ).first()

    if existing_edge:
        raise HTTPException(
            status_code=400,
            detail="Edge already exists between these nodes"
        )

    new_edge = models.Edge(
        source=edge.source,
        destination=edge.destination,
        latency=edge.latency
    )

    db.add(new_edge)
    db.commit()
    db.refresh(new_edge)

    return new_edge

@router.get("/edges", response_model=list[schemas.EdgeResponse])
def get_edges(db: Session = Depends(get_db)):
    edges = db.query(models.Edge).all()

    return edges

@router.post("/routes/shortest", response_model=schemas.RouteResponse)
def get_shortest_route(req: schemas.RouteRequest, db: Session = Depends(get_db)):

    source_node = db.query(models.Node).filter(
        models.Node.name == req.source
    ).first()

    destination_node = db.query(models.Node).filter(
        models.Node.name == req.destination
    ).first()

    if not source_node or not destination_node:
        raise HTTPException(
            status_code=400,
            detail="Invalid source or destination node"
        )

    edges = db.query(models.Edge).all()

    latency, path = shortest_path(edges, req.source, req.destination)

    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"No path exists between {req.source} and {req.destination}"
        )

    history = models.RouteHistory(
        source=req.source,
        destination=req.destination,
        total_latency=latency,
        path=",".join(path)
    )

    db.add(history)
    db.commit()

    return {
        "total_latency": latency,
        "path": path
    }

@router.get("/routes/history")
def get_route_history(
    source: str | None = Query(None),
    destination: str | None = Query(None),
    limit: int | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(models.RouteHistory)

    if source:
        query = query.filter(models.RouteHistory.source == source)

    if destination:
        query = query.filter(models.RouteHistory.destination == destination)

    if date_from:
        query = query.filter(
            models.RouteHistory.created_at >= datetime.fromisoformat(date_from)
        )

    if date_to:
        query = query.filter(
            models.RouteHistory.created_at <= datetime.fromisoformat(date_to)
        )

    query = query.order_by(models.RouteHistory.created_at.desc())

    if limit:
        query = query.limit(limit)

    history_records = query.all()

    results = []

    for record in history_records:
        results.append({
            "id": record.id,
            "source": record.source,
            "destination": record.destination,
            "total_latency": record.total_latency,
            "path": record.path.split(","),
            "created_at": record.created_at
        })

    return results