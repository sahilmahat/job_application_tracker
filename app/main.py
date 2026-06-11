from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import store
from .models import ApplicationCreate, ApplicationUpdate, Application
from .database import engine, get_db, Base
from . import db_models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/applications", response_model=list[Application])
def list_applications(db: Session = Depends(get_db)):
    return store.list_all(db)


@app.get("/applications/{app_id}", response_model=Application)
def get_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = store.get(db, app_id)
    if app_obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@app.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    return store.create(db, data)


@app.patch("/applications/{app_id}", response_model=Application)
def update_application(app_id: int, data: ApplicationUpdate, db: Session = Depends(get_db)):
    updated = store.update(db, app_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated


@app.delete("/applications/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    deleted = store.delete(db, app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")


app.mount("/", StaticFiles(directory="static", html=True), name="static")