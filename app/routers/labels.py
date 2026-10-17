from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Label
from app.schemas import LabelCreate, LabelRead, LabelUpdate

router = APIRouter(prefix="/v1/labels", tags=["labels"])


@router.get("", response_model=list[LabelRead])
def list_labels(db: Session = Depends(get_db)):
    return db.scalars(select(Label).order_by(Label.id)).all()


@router.get("/{label_id}", response_model=LabelRead)
def get_label(label_id: int, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if label is None:
        raise HTTPException(404, "Метка не найдена")
    return label


@router.post("", response_model=LabelRead, status_code=201)
def create_label(payload: LabelCreate, db: Session = Depends(get_db)):
    label = Label(**payload.model_dump())
    db.add(label)
    db.commit()
    db.refresh(label)
    return label


@router.patch("/{label_id}", response_model=LabelRead)
def update_label(label_id: int, payload: LabelUpdate, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if label is None:
        raise HTTPException(404, "Метка не найдена")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(label, key, value)
    db.commit()
    db.refresh(label)
    return label


@router.delete("/{label_id}", status_code=204)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    label = db.get(Label, label_id)
    if label is None:
        raise HTTPException(404, "Метка не найдена")
    db.delete(label)
    db.commit()
    return Response(status_code=204)