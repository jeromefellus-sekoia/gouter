import jwt
from fastapi import HTTPException
from fastapi import Request, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from api.utils import SECRETS, adapt_signature


class Session(BaseModel):
    email: str
    username: str


def session(request: Request) -> Session | None:
    if os.getenv("ENV") != "prod":
        return Session(email="someone@sekoia.io", username="someone")

    try:
        return Session.parse_obj(
            jwt.decode(request.cookies["session"], SECRETS["SECRET_KEY"], ["HS256"])
        )
    except Exception:
        return None


def login_from_google(token: str):
    x = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        os.environ["GOOGLE_CLIENT_ID"],
    )

    if x["hd"] not in ["sekoia.fr", "sekoia.io"]:
        raise PermissionError("Wrong domain")

    return (
        jwt.encode(
            Session(email=x["email"], username=x["name"]).dict(),
            SECRETS["SECRET_KEY"],
            "HS256",
        ),
        x,
    )


def authenticated(f):
    def wrapped(*args, __session: Session | None = Depends(session), **kw):
        if not __session:
            raise HTTPException(401, "Unauthenticated")
        return f(*args, **kw)

    return adapt_signature(wrapped, f)
