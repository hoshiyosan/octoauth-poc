from octoauth.architecture.dao import BaseDAO
from octoauth.database import Application


class ApplicationDAO(BaseDAO):
    model = Application
