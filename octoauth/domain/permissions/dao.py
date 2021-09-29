from octoauth.architecture.dao import BaseDAO
from octoauth.database import Permission


class PermissionDAO(BaseDAO):
    model = Permission
