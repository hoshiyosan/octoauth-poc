from fastapi import FastAPI

import octoauth.domain.application.views


class API(FastAPI):
    def __init__(self):
        super().__init__(
            title="OctoAuth",
            description="An home made Oauth2 server for small to medium companies.",
            version="0.1b",
        )
        self.register_routers()

    def register_routers(self):
        self.include_router(
            octoauth.domain.application.views.router, tags=["applications"]
        )


api = API()
