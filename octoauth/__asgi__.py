"""
Defines application metadata, routes and middlewares
"""
import json
import uuid
from urllib.parse import urlencode

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

import octoauth.domain.applications.views
import octoauth.domain.authenticate.views
import octoauth.domain.authorize.views
from octoauth.architecture.database import Session
from octoauth.database import Application, DBModel, Permission
from octoauth.domain.authorize.errors import AuthorizationError


class API(FastAPI):
    def __init__(self):
        super().__init__(
            title="OctoAuth", description="An home made Oauth2 server for small to medium companies.", version="0.1b"
        )
        self.initialize_database()

        self.register_routers()
        self.register_templates()
        self.register_middlewares()
        self.register_error_handlers()

    def initialize_database(self):
        DBModel.metadata.drop_all()
        DBModel.metadata.create_all()

        with Session() as session:
            application = Application(
                client_id="sortify",
                name="Sortify",
                description="An application to sort your playlists from Spotify, Deezer or Youtube.",
                authorized_redirect_uris="https://sortify.sylvan.ovh/authorized",
                icon_uri="http://play.sylvan.ovh/favicon.ico",
            )
            session.add(application)
            session.commit()

            scope = Permission(code="admin", name="Administrator", description="Grant full access to this app")
            session.add(scope)
            session.commit()

            print(application.client_id)

    def register_routers(self):
        self.include_router(octoauth.domain.applications.views.router, tags=["applications"])
        self.include_router(octoauth.domain.authenticate.views.router, tags=["authenticate"])
        self.include_router(octoauth.domain.authorize.views.router, tags=["authorize"])

    def register_templates(self):
        octoauth.domain.authenticate.views.templates.init_app(self)
        octoauth.domain.authorize.views.templates.init_app(self)

    def register_middlewares(self):
        self.add_middleware(CORSMiddleware)

    def register_error_handlers(self):
        @self.exception_handler(AuthorizationError)
        def authorization_error_handler(request, error: AuthorizationError):
            return RedirectResponse(
                url="/authorize/error?" + urlencode({"path": request.url._url, "messages": ";".join(error.messages)})
            )

        @self.exception_handler(RequestValidationError)
        def validation_exception_handler(request, error: RequestValidationError):
            exc_info = json.loads(error.json())
            if request.url.path == "/authorize":
                error_messages = []
                for info in exc_info:
                    if info["loc"][0] == "query" and info["type"] == "value_error.missing":
                        message = "Missing query parameter '%s'" % info["loc"][1]
                    else:
                        message = info
                    error_messages.append(message)
                return authorization_error_handler(request, AuthorizationError(error_messages))
            return JSONResponse({"detail": exc_info})


api = API()
