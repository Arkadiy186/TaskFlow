from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import comments, labels, projects, tasks, users

app = FastAPI(title="Team Tasks API")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(labels.router)
app.include_router(tasks.router)
app.include_router(comments.router)

MESSAGES = {
    "23505": "Запись с таким уникальным значением уже существует",
    "23503": "Нарушена связь между записями: указанная запись не существует "
             "или на неё ссылаются другие записи",
}


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    code = getattr(exc.orig, "sqlstate", None)
    detail = MESSAGES.get(code, "Нарушено ограничение целостности данных")
    return JSONResponse(status_code=409, content={"detail": detail})


@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(select(1))
    except Exception:
        raise HTTPException(503, "База данных недоступна")
    return {"status": "ok"}