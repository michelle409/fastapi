from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, posts, users, votes

app = FastAPI(title="Community Posts API", version="1.0.0", description="A learning project for authenticated posts, users and voting.")

app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to the Community Posts API"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
