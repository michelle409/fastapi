from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Post, User, Vote
from ..schemas import PostCreate, PostOut, PostWithVotes

router = APIRouter(prefix="/posts", tags=["Posts"])


def _post_or_404(db: Session, post_id: int) -> Post:
    post = db.scalar(select(Post).options(joinedload(Post.owner)).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} was not found")
    return post


@router.get("/", response_model=list[PostWithVotes])
def get_posts(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), search: str = "", db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vote_count = func.count(Vote.post_id).label("votes")
    statement = (select(Post, vote_count).outerjoin(Vote, Vote.post_id == Post.id)
                 .options(joinedload(Post.owner)).where(Post.title.contains(search))
                 .group_by(Post.id).order_by(Post.created_at.desc(), Post.id.desc())
                 .limit(limit).offset(skip))
    rows = db.execute(statement).unique().all()
    return [{"Post": post, "votes": count} for post, count in rows]


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = Post(owner_id=current_user.id, **payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return _post_or_404(db, post.id)


@router.get("/{post_id}", response_model=PostWithVotes)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = _post_or_404(db, post_id)
    count = db.scalar(select(func.count(Vote.post_id)).where(Vote.post_id == post_id)) or 0
    return {"Post": post, "votes": count}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = _post_or_404(db, post_id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = _post_or_404(db, post_id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    for field, value in payload.model_dump().items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return _post_or_404(db, post_id)
