import os
import posixpath
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader


class Templates:
    def __init__(self, module_name: str, assets_namespace: str = "/"):
        package_directory = os.path.abspath(os.path.dirname(sys.modules[module_name].__file__))
        self.templates_path = os.path.join(package_directory, "templates")
        self.assets_path = os.path.join(package_directory, "assets")
        self.assets_prefix = posixpath.join("/static", assets_namespace.lstrip("/"))

    def init_app(self, app: FastAPI):
        self.environment = Environment(loader=FileSystemLoader(self.templates_path))
        app.mount(self.assets_prefix, StaticFiles(directory=self.assets_path))

    def get_asset_url(self, filepath: str) -> str:
        return posixpath.join(self.assets_prefix, filepath)

    def render(self, template_name: str, **context) -> HTMLResponse:
        template = self.environment.get_template(template_name)
        return HTMLResponse(template.render(asset_url=self.get_asset_url, **context))
