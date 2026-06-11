from fastapi import FastAPI, HTTPException, status

from .models import ApplicationCreate, ApplicationUpdate, Application
from .store import store

app = FastAPI(title="Job Application Tracker")

@app.get("/applications", response_model=list[Application])
def list_application():
    return store.list_all()

@app.get("/applications/{app_id}", response_model=Application)
def get_application(app_id : int):
    app_obj = store.get(app_id)
    if app_obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj

@app.post("/applications", response_model = Application, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate):
    return store.create(data)

@app.patch("/applications/{app_id}", response_model= Application)
def Update_application(app_id:int, data: ApplicationUpdate):
    updated = store.update(app_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated

@app.delete("/applications/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(app_id: int):
    deleted = store.delete(app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    
