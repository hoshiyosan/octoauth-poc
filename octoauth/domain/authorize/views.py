import json

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from octoauth.architecture.dao import ObjectNotFoundError
from octoauth.architecture.database import Session
from octoauth.architecture.templates import Templates
from octoauth.database import Permission
from octoauth.domain.applications import ApplicationDAO, ApplicationReadDTO
from octoauth.domain.authorize.errors import AuthorizationError
from octoauth.domain.permissions import PermissionDAO

router = APIRouter()
templates = Templates(__name__, assets_namespace="/authorize")


@router.get("/authorize")
def login_view(response_type: str, client_id: str, redirect_uri: str, scope: str, state: str):
    with Session() as session:
        application_dao = ApplicationDAO(session)
        permission_dao = PermissionDAO(session)

        try:
            application = application_dao.get_or_404(client_id=client_id)
            permissions = permission_dao.search(Permission.code.in_(scope.strip(",").split(",")))
        except ObjectNotFoundError:
            raise AuthorizationError("No application found with client_id: %s" % client_id)

        if redirect_uri not in application.authorized_redirect_uris:
            raise AuthorizationError("Invalid redirect_uri")

    return templates.render("authorize.html", application=application, permissions=permissions)


@router.get("/authorize/error")
def login_error_view(path: str, messages: str):
    return templates.render("error.html", error_path=path, messages=messages.split(";"))
