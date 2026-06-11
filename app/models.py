from datetime import date ,datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Status(str, Enum):
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    rejected = "rejected"

class ApplicationCreate(BaseModel):
    company : str
    role : str
    status: Status
    applied_date : date

class ApplicationUpdate(BaseModel):
    company : Optional[str] = None
    role : Optional[str] = None
    status : Optional[Status] = None
    applied_date : Optional[date] = None


class Application(BaseModel):
    id : int
    company : str
    role : str
    status : Status
    applied_date : date
    created_at : datetime
    updated_at : datetime