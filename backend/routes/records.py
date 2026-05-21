"""Analysis record routes for browsing stored waste detection history."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database.db import get_db
from database.models import AnalysisRecord

router = APIRouter()


@router.get("")
def list_records(db: Session = Depends(get_db)):
    records = (
        db.query(AnalysisRecord)
        .options(joinedload(AnalysisRecord.items))
        .order_by(AnalysisRecord.created_at.desc())
        .all()
    )
    return records


@router.get("/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(AnalysisRecord)
        .options(joinedload(AnalysisRecord.items))
        .filter(AnalysisRecord.record_id == record_id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
