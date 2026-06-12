# Job Application Tracker

A simple web app to track job applications — add them, update their status as you
progress, and delete the ones you no longer need. Built as a three-tier
application (frontend, API, database) and fully containerized with Docker.

## What it does

- Add a job application with company, role, status, and the date you applied
- See all your applications in one list
- Update an application's status as it moves along (applied → interviewing → offer → rejected)
- Delete applications you no longer want to track

Your data is stored in PostgreSQL and persists across restarts.

## Architecture

The app runs as four containers wired together with Docker Compose:

```
Browser  →  nginx  →  FastAPI  →  PostgreSQL
            (port 80)  (API)      (database)
```

- **nginx** — the front door. Serves the web page and forwards `/api` requests to the backend.
- **FastAPI** — the backend API. Handles all the application logic and talks to the database.
- **PostgreSQL** — stores the application data, in a Docker volume that survives restarts.
- **Frontend** — plain HTML, CSS, and JavaScript served by nginx.

## Tech stack

- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python, FastAPI, SQLAlchemy
- Database: PostgreSQL
- Reverse proxy: nginx
- Containerization: Docker, Docker Compose

## Requirements

You only need Docker installed:

- Docker
- Docker Compose

Nothing else — Python, PostgreSQL, and all dependencies run inside containers.

## How to run

1. Clone the repository:

   ```
   git clone https://github.com/sahilmahat/job_application_tracker.git
   cd job_application_tracker
   ```

2. Build and start everything:

   ```
   docker compose up --build
   ```

   The first run takes a minute or two while images are built. You'll see the
   database start, then the API, then nginx.

3. Open the app in your browser:

   ```
   http://localhost
   ```

That's it — the app is running.

To stop it, press `Ctrl+C` in the terminal, then:

```
docker compose down
```

This stops the containers but keeps your data. To also delete the stored data,
use `docker compose down -v` (this wipes the database).

## How to use

1. Open `http://localhost` in your browser.
2. Fill in the form at the top — company, role, status, and applied date — then click **Add**.
3. Your application appears in the list below.
4. To change a status, use the dropdown in that application's row. It updates automatically.
5. To remove an application, click **Delete** in its row.

## Project structure

```
job_application_tracker/
├── app/
│   ├── main.py          # FastAPI app and endpoints
│   ├── models.py        # Pydantic models (request/response shapes)
│   ├── db_models.py     # SQLAlchemy model (database table)
│   ├── database.py      # Database connection setup
│   └── store.py         # Data operations (CRUD)
├── static/
│   └── index.html       # The frontend (HTML, CSS, JS)
├── nginx.conf           # nginx reverse proxy config
├── Dockerfile           # Builds the API image
├── docker-compose.yaml  # Defines all four services
├── requirements.txt     # Python dependencies
└── DESIGN.md            # Design document
```

## API endpoints

The backend exposes a simple REST API (reached through nginx at `/api`):

| Method | Path                  | Description              |
|--------|-----------------------|--------------------------|
| GET    | `/applications`       | List all applications    |
| GET    | `/applications/{id}`  | Get one application      |
| POST   | `/applications`       | Create an application    |
| PATCH  | `/applications/{id}`  | Update an application    |
| DELETE | `/applications/{id}`  | Delete an application    |

## Notes

- Database credentials are set in `docker-compose.yaml` for local development.
  For a real deployment, these should be moved to secrets or environment files
  that are not committed to version control.
- The database data lives in a Docker named volume (`pgdata`), so it persists
  even when containers are stopped and recreated.
