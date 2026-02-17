from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import Select
from sqlalchemy.orm import Session

from db import engine, get_db
from models import Base, Url
from schemas import UrlCreate, UrlResponse
from services import encode

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/home")
def home():
    return {"hello": "world"}


@app.post("/short_url", response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    url_in: UrlCreate,
    session: Annotated[Session, Depends(get_db)],
):
    url = Url(original_url=str(url_in.original_url))
    session.add(url)
    session.flush()
    url.short_code = encode(url.id)
    url.expires_at = url.created_at + timedelta(days=7)
    session.commit()
    return url


@app.get("/{short_code}")
def redirect(short_code: str, session: Annotated[Session, Depends(get_db)]):
    stmt = Select(Url).where(Url.short_code == short_code)
    url: Url = session.execute(stmt).scalars().one_or_none()
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No redirect url found",
        )
    if url.expires_at and url.expires_at.replace(tzinfo=UTC) < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL expired")
    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
