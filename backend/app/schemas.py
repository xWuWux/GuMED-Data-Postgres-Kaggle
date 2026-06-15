from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class HeartDiseaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:       int
    age:      int
    sex:      int
    cp:       int
    trestbps: Optional[int]   = None
    chol:     Optional[int]   = None
    fbs:      Optional[int]   = None
    restecg:  Optional[int]   = None
    thalach:  Optional[int]   = None
    exang:    Optional[int]   = None
    oldpeak:  Optional[float] = None
    slope:    Optional[int]   = None
    ca:       Optional[float] = None
    thal:     Optional[float] = None
    target:   int

class StatsResponse(BaseModel):
    total_records: int
    heart_disease_positive: int
    heart_disease_negative: int
    average_age: float
