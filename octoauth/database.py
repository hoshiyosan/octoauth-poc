# pylint: disable=too-few-public-methods
"""
Defines SQLAlchemy models used to create and query database tables.
"""
from typing import List

from sqlalchemy import Boolean, Column, String

from octoauth.architecture.database import DBModel


class Application(DBModel):
    """
    Represents a client application in Oauth2 protocol
    """

    __tablename__ = "application"
    icon_uri = Column(String, nullable=True)
    client_id = Column(String(36), primary_key=True)
    is_public = Column(Boolean, default=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(300))
    authorized_redirect_uris = Column(String)  # coma separated list of uris


class Role(DBModel):
    """
    A role is an abstraction used to create a collection of permissions.
    """

    __tablename__ = "role"
    uid = Column(String(36), primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(300))


class Permission(DBModel):
    """
    A permission defines if a subject can do something specific in an app.
    """

    __tablename__ = "permission"
    code = Column(String(80), primary_key=True)
    name = Column(String(80))
    description = Column(String(300))


class RoleHasPermission(DBModel):
    """
    Association table that defines mapping between roles and permissions.
    """

    __tablename__ = "role_permission"
    role_uid = Column(String(36), primary_key=True)
    application_uid = Column(String(36), primary_key=True)
    permission_uid = Column(String(36), primary_key=True)
