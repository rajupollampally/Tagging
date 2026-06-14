from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db, init_db
from app.models.story import Story
from app.security import get_current_user, get_approver_user, get_admin_user
from app.utils.logger import logger

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.strip('[]').split(',')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Application startup completed")

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}

@app.post("/stories", status_code=status.HTTP_201_CREATED)
async def create_story(payload: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if "title" not in payload or "completion_month" not in payload or "target_release_month" not in payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required story fields")

    story = Story(
        title=payload["title"],
        description=payload.get("description", ""),
        completion_month=payload["completion_month"],
        target_release_month=payload["target_release_month"],
        owner=payload.get("owner", current_user.get("email")),
        status=payload.get("status", "open")
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story

@app.get("/stories")
async def list_stories(db: Session = Depends(get_db)):
    return db.query(Story).all()

@app.get("/stories/{story_id}")
async def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    return story

@app.put("/stories/{story_id}")
async def update_story(story_id: int, payload: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    if story.owner != current_user.get("email") and current_user.get("role") not in ["admin", "approver"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to update story")

    story.title = payload.get("title", story.title)
    story.description = payload.get("description", story.description)
    story.completion_month = payload.get("completion_month", story.completion_month)
    story.target_release_month = payload.get("target_release_month", story.target_release_month)
    story.status = payload.get("status", story.status)
    db.commit()
    db.refresh(story)
    return story

@app.delete("/stories/{story_id}")
async def delete_story(story_id: int, current_user: dict = Depends(get_admin_user), db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    db.delete(story)
    db.commit()
    return {"detail": "Story deleted"}
