from sqlalchemy.orm import Session

from .db_models import ApplicationRow
from .models import ApplicationCreate, ApplicationUpdate


def list_all(db: Session) -> list[ApplicationRow]:
    return db.query(ApplicationRow).all()


def get(db: Session, app_id: int) -> ApplicationRow | None:
    return db.query(ApplicationRow).filter(ApplicationRow.id == app_id).first()


def create(db: Session, data: ApplicationCreate) -> ApplicationRow:
    row = ApplicationRow(
        company=data.company,
        role=data.role,
        status=data.status,
        applied_date=data.applied_date,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, app_id: int, data: ApplicationUpdate) -> ApplicationRow | None:
    row = db.query(ApplicationRow).filter(ApplicationRow.id == app_id).first()
    if row is None:
        return None
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete(db: Session, app_id: int) -> bool:
    row = db.query(ApplicationRow).filter(ApplicationRow.id == app_id).first()
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True