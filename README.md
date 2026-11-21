# Community Posts API

An independently implemented learning project based on the requirements explored in the FastAPI course repository by Sanjeev Thiyagarajan. The project provides a JWT-protected posts API with user registration, post CRUD, voting, SQLAlchemy persistence, Alembic migrations and automated tests. The course repository is the learning reference; this codebase is a separate implementation.

## Features
- Register users and retrieve a user by ID.
- Log in using OAuth2 password form and receive a JWT bearer token.
- Create, list, search, retrieve, update and delete posts.
- Add or remove one vote per user per post.
- Paginate posts using `limit` and `skip`.
- SQLite works out of the box; PostgreSQL is supported through `DATABASE_URL`.
- Alembic schema migrations and pytest tests.

## macOS / VS Code setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

The example `.env` uses SQLite, so no separate database server is required to start locally.

## Database

Create the tables with Alembic:

```bash
alembic upgrade head
```

To use PostgreSQL instead, create a database named `community_posts`, then edit `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/community_posts
```

Run `alembic upgrade head` again after changing the database URL.

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

## Main endpoints

| Method | Path | Purpose | Authentication |
|---|---|---|---|
| GET | `/` | Welcome message | No |
| GET | `/health` | Health check | No |
| POST | `/users/` | Register | No |
| GET | `/users/{user_id}` | User details | No |
| POST | `/login` | Obtain JWT | No |
| GET | `/posts/` | List/search posts (`limit`, `skip`, `search`) | Yes |
| POST | `/posts/` | Create post | Yes |
| GET | `/posts/{post_id}` | Get post and vote count | Yes |
| PUT | `/posts/{post_id}` | Update own post | Yes |
| DELETE | `/posts/{post_id}` | Delete own post | Yes |
| POST | `/vote/` | Add (`dir: 1`) or remove (`dir: 0`) a vote | Yes |

For login, Swagger's OAuth2 form expects the email in the `username` field and the account password in `password`. Click **Authorize** and enter the credentials to test protected routes.

## Tests

```bash
pytest -q
```

## Security notes
- Copy `.env.example` to `.env`; never commit `.env`.
- Replace `SECRET_KEY` with a long random secret before deployment. Generate one with `openssl rand -hex 32`.
- Passwords are hashed using Argon2.
- CORS origins should be restricted to the frontend domains you control.

## Learning reference
Original course repository: https://github.com/Sanjeev-Thiyagarajan/fastapi-course
