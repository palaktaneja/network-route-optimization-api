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