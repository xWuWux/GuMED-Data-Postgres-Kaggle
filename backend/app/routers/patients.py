from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from ..database import get_db
from ..models import HeartDisease
from ..schemas import HeartDiseaseResponse, StatsResponse

router = APIRouter()

@router.get("/patients", response_model=List[HeartDiseaseResponse])
async def list_patients(
    skip:   int            = Query(default=0,   ge=0),
    limit:  int            = Query(default=100, le=1000),
    target: Optional[int]  = Query(default=None, description="0=healthy, 1=disease"),
    db:     AsyncSession   = Depends(get_db)
):
    query = select(HeartDisease)
    if target is not None:
        query = query.where(HeartDisease.target == target)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/patients/stats/summary", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    total    = (await db.execute(select(func.count(HeartDisease.id)))).scalar()
    positive = (await db.execute(
        select(func.count(HeartDisease.id)).where(HeartDisease.target == 1)
    )).scalar()
    avg_age  = (await db.execute(select(func.avg(HeartDisease.age)))).scalar()
    return StatsResponse(
        total_records=total,
        heart_disease_positive=positive,
        heart_disease_negative=total - positive,
        average_age=round(avg_age or 0, 1)
    )

@router.get("/patients/{patient_id}", response_model=HeartDiseaseResponse)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result  = await db.execute(
        select(HeartDisease).where(HeartDisease.id == patient_id)
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
