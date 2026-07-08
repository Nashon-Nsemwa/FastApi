# SocialMedia FastAPI Backend

## Overview

This repository contains a FastAPI backend project built with PostgreSQL, SQLAlchemy, Alembic migrations, JWT authentication, and Docker containerization.

The application exposes CRUD endpoints for posts, user registration and login, and vote management. It is structured as a modular FastAPI service with separate routers, database configuration, models, and Pydantic schemas.

## Architecture

### Core components

- `app/main.py` - FastAPI application setup, CORS middleware, router registration, and root endpoint.
- `app/config.py` - Environment-based settings using `pydantic-settings`.
- `app/database.py` - SQLAlchemy engine, session factory, declarative base, and `get_db()` dependency.
- `app/models.py` - SQLAlchemy ORM models for `Post`, `User`, and `Vote`.
- `app/schemas.py` - Pydantic schemas for request validation and response models.
- `app/oauth2.py` - JWT creation, verification, and authentication dependency.
- `app/utils.py` - Password hashing and verification utilities.
- `app/routers/` - FastAPI routers grouped by feature:
  - `post.py` - post CRUD and list endpoints
  - `user.py` - user creation and retrieval
  - `auth.py` - login and token generation
  - `vote.py` - vote and unvote functionality

## File Structure

```
FASTAPI/
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── vote.py
│   ├── schemas.py
│   └── utils.py
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── alembic.ini
├── Procfile
└── .env
```

## Database and ORM

### SQLAlchemy models

- `Post`
  - `id`, `title`, `content`, `published`, `created_at`, `owner_id`
  - `owner_id` is a foreign key to `users.id`
  - `owner` relationship to `User`

- `User`
  - `id`, `email`, `password`, `created_at`, `phone_number`

- `Vote`
  - Composite primary key: `user_id`, `post_id`
  - Foreign keys to `users.id` and `posts.id`

### Pydantic schemas

- `PostBase`, `PostCreate`, `Post`, `PostOut`
- `UserCreate`, `UserOut`, `UserLogin`
- `Token`, `TokenData`
- `Vote`

The schemas ensure request payload validation and response formatting.

## Authentication

- JWT tokens are created in `app/oauth2.py`.
- `create_access_token()` signs data with `SECRET_KEY`, `ALGORITHM`, and expiration.
- `get_current_user()` validates tokens from the `Authorization: Bearer` header.
- `login` endpoint uses `OAuth2PasswordRequestForm` and returns `access_token` and `token_type`.

## Migrations

Alembic is configured in `alembic/` and `alembic.ini`.

Typical migration workflow:

```bash
alembic revision --autogenerate -m "Add migration message"
alembic upgrade head
```

> Note: `app/main.py` currently comments out `models.Base.metadata.create_all(bind=engine)`, which is correct when using Alembic.

## Docker Implementation

### Dockerfile

The `dockerfile` builds the application image:

```dockerfile
FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8800" ]
```

### docker-compose.yml

The Compose setup defines two services: `api` and `postgres`.

Correct `postgres` service configuration:

```yaml
version: '4'
services:
  api:
    build: .
    container_name: fastapi
    ports:
      - "8800:8800"
  postgres:
    image: postgres:15
    container_name: postgres-Fastapi
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 12345678
      POSTGRES_DB: FASTAPI
    volumes:
      - postgres-db:/var/lib/postgresql/data

volumes:
  postgres-db:
```

### `.env` variables

Create a `.env` file in the repo root with the following values:

```env
database_hostname=postgres
database_port=5432
database_name=FASTAPI
database_username=postgres
database_password=12345678
secret_key=YOUR_SECRET_KEY
algorithm=HS256
access_token_expire_minutes=30
```

## Run with Docker

Build and start the containers:

```bash
docker compose up -d --build
```

Run the Alembic migrations inside the `api` container:

```bash
docker compose exec api alembic upgrade head
```

Open the API at:

```text
http://localhost:8800
```

## API Endpoints

- `GET /` — health check / root endpoint
- `POST /users/` — create a new user
- `GET /users/{id}` — retrieve user by ID
- `POST /login` — authenticate and receive JWT token
- `GET /posts/` — list posts with vote counts (requires auth)
- `POST /posts/` — create a new post (requires auth)
- `GET /posts/{id}` — get a post by ID with votes (requires auth)
- `PUT /posts/{id}` — update a post (requires auth and ownership)
- `DELETE /posts/{id}` — delete a post (requires auth and ownership)
- `POST /vote/` — vote or remove vote on a post (requires auth)

## Notes

- The `api` service listens on port `8800`.
- The project expects a PostgreSQL database available at the hostname `postgres` when run from Docker Compose.
- Passwords are hashed using `bcrypt` in `app/utils.py`.

## Useful commands

```bash
# Start docker services
docker compose up -d --build

# Stop services
docker compose down

# Enter api container shell
docker compose exec api sh

# Run migrations
docker compose exec api alembic upgrade head
```

## Dependencies

See `requirements.txt` for the full Python dependency list, including FastAPI, SQLAlchemy, Alembic, Pydantic, psycopg2-binary, python-jose, bcrypt, and uvicorn.
