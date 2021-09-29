from fastapi import APIRouter

from octoauth.architecture.database import Session
from octoauth.architecture.templates import Templates

router = APIRouter()
templates = Templates(__name__, assets_namespace="/auth")


@router.get("/login")
def login_view():
    return templates.render("login.html")
