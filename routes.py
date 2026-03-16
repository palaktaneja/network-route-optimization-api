from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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