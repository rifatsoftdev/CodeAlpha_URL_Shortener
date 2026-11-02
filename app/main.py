from datetime import datetime, timedelta, timezone
import secrets

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


from app.database import engine, Base, get_db
from app.models import URL
from app.schema import URLCreate



URL_LIFETIME = timedelta(days=14)


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="URL Shortener Server"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/{url}")
def get_real_url(url: str, request: Request, db: Session = Depends(get_db)):

    short_url = db.query(URL).filter(
        URL.short_code == url
    ).first()

    if short_url is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404,
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if short_url.expires_at is not None and short_url.expires_at <= now:
        db.delete(short_url)
        db.commit()

        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404,
        )

    short_url.click_count = (short_url.click_count or 0) + 1
    db.commit()

    return RedirectResponse(
        url=short_url.original_url
    )


@app.post("/add-new-url")
@limiter.limit("10/minute")
def add_new_url(payload: URLCreate, request: Request, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    db.query(URL).filter(
        URL.expires_at <= now
    ).delete(synchronize_session=False)

    short_code = secrets.token_urlsafe(6)

    while db.query(URL.id).filter(URL.short_code == short_code).first() is not None:
        short_code = secrets.token_urlsafe(6)

    short_url = URL(
        original_url=str(payload.url),
        short_code=short_code,
        expires_at=now + URL_LIFETIME,
    )
    db.add(short_url)
    db.commit()

    return {"short_url": f"{str(request.base_url).rstrip('/')}/{short_code}"}






# =====================================================================================
# =====================================================================================