# Mini Ticket Tracker API

#### Create a virtual environment:
```bash
python -m venv .venv
```
#### Activate the virtual environment:

Linux / macOS
```bash
source .venv/bin/activate
```
Windows PowerShell
```bash
.venv\Scripts\Activate.ps1
```
#### Install dependencies:
```bash
pip install "fastapi[standard]" "sqlalchemy>=2.0,<3.0" "psycopg[binary]" alembic pydantic-settings

or

uv add "fastapi[standard]" "sqlalchemy>=2.0,<3.0" "psycopg[binary]" alembic pydantic-settings
```
#### Test the API:
```bash
uv run fastapi dev

or

fastapi dev app/main.py 
```
#### Set up PostgreSQL:
Create a PostgreSQL database and a dedicated user for the API. For example, connect to PostgreSQL as an administrator and execute:
```bash
CREATE USER ticket_user WITH PASSWORD 'password';

CREATE DATABASE ticket_db OWNER ticket_user;
```
Alternatively just use pgAdmin4 to create user and the database
#### Create .env and store the connection URL in .env:
```bash
DATABASE_URL=postgresql+psycopg://ticket_user:password@localhost:5432/ticket_db
```
#### Initialize Alembic:
```bash
alembic init migrations
```
#### Configure Alembic database migrations:
1. Open alembic.ini and find sqlalchemy.url
2. Edit migrations/env.py to use your application settings and model metadata. Keep the other generated Alembic functions, but update the imports and target_metadata

```bash
from app.config import settings
from app.database import Base
from app.models import Ticket

config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)

target_metadata = Base.metadata
```
#### Generate the first migration:
```bash
alembic revision --autogenerate -m "create tickets table"
```
A folder named migrations should be created in the root directory.
Review the generated file inside migrations/versions/. It should create the tickets table, its enum types, and indexes.
#### Apply the migration:
```bash
alembic upgrade head
```
This should now create the table to your database
#### Re-run the API to test endpoints:
```bash
uv run fastapi dev

or

fastapi dev app/main.py 
```
#### On your browser use the link to view the API documentation and execute tests:
Expand an endpoint and click 'Try it out' button, provide required payload and execute the endpoint
```bash
http://127.0.0.1:8000/docs
```
### Decisions & Tradeoffs
1. I would recommend uv instead of traditional pip for dependency management and API execution
2. Assuming the ticketing system is to be used to manage projects and business, I would include extra entities and establish relationships between those entities such as users, authentication, ticket history e.t.c
3. I used AI as my helper to speed up my development.
4. I would also use AI to scale the project.
5. I chose to use python FastAPI because it is a modern, high-performance, scalable framework. 
