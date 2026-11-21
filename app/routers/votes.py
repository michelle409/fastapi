from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Post, User, Vote
from ..schemas import VoteCreate

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def cast_vote(payload: VoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.get(Post, payload.post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {payload.post_id} does not exist")
    existing = db.get(Vote, (current_user.id, payload.post_id))
    if payload.dir == 1:
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {payload.post_id}")
        db.add(Vote(user_id=current_user.id, post_id=payload.post_id))
        db.commit()
        return {"message": "successfully added vote"}
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
    db.delete(existing)
    db.commit()
    return {"message": "successfully deleted vote"}
