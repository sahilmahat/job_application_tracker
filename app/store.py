from datetime import date, datetime, timezone
from .models import ApplicationCreate, ApplicationUpdate, Application

class ApplicationStore:
    def __init__(self):
        self._items: dict[int, Application] = {}
        self._next_id: int = 1

    def list_all(self) -> list[Application]:
        return list(self._items.values())
    
    def get(self, app_id: int) -> Application | None:
        return self._items.get(app_id)
    
    def create(self, data: ApplicationCreate) -> Application:
        now = datetime.now(timezone.utc)
        app = Application(
            id = self._next_id,
            company = data.company,
            role = data.role,
            status = data.status,
            applied_date = data.applied_date,
            created_at = now,
            updated_at = now
        )
        self._items[app.id] = app
        self._next_id += 1
        return app

    def update(self, app_id: int, data: ApplicationUpdate) -> Application | None:
        existing = self._items.get(app_id)
        if existing is None:
            return None
        changes = data.model_dump(exclude_unset = True)
        updated = existing.model_copy(update=changes)
        updated.updated_at = datetime.now(timezone.utc)
        self._items[app_id]= updated
        return updated
    
    def delete(self, app_id: int) -> bool:
        if app_id not in self._items:
            return False
        del self._items[app_id]
        return True
    
store = ApplicationStore()
