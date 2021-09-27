from sqlalchemy import Column, String

from octoauth.architecture.database import DBModel


class Role(DBModel):
    __tablename__ = "roles"
    uid = Column(String(36), primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(300))


class Permission(DBModel):
    __tablename__ = "permissions"
    uid = Column(String(36), primary_key=True)
    code = Column(String(80), unique=True)
    title = Column(String(80))
    description = Column(String(300))


class Application(DBModel):
    __tablename__ = "applications"
    uid = Column(String(36), primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(300))


class RoleHasPermission(DBModel):
    __tablename__ = "role_permissions"
    role_uid = Column(String(36), primary_key=True)
    application_uid = Column(String(36), primary_key=True)
    permission_uid = Column(String(36), primary_key=True)
