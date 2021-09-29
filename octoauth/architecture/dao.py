from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from octoauth.architecture.database import DBModel


class DAOException(Exception):
    ...


class ObjectNotFoundError(DAOException):
    ...


class BaseDAO:
    session: Session
    model: DBModel

    def __init__(self, session: Session):
        self.session = session

    def __query(self, *complex_filters, **simple_filters):
        return self.session.query(self.model).filter(*complex_filters).filter_by(**simple_filters)

    def get_or_404(self, *complex_filters, **simple_filters) -> "model":
        instance = self.__query(*complex_filters, **simple_filters).first()
        if instance is None:
            raise ObjectNotFoundError("%s not found." % self.model.__tablename__)
        return instance

    def search(self, *complex_filters, **simple_filters) -> List["model"]:
        return self.__query(*complex_filters, **simple_filters).all()

    def create(self, **properties):
        instance = self.model(**properties)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, instance_uid: str, **properties):
        instance = self.get_or_404(uid=instance_uid)
        for attr, value in properties.items():
            setattr(instance, attr, value)
        self.session.commit()
        return instance

    def delete(self, instance_uid: str):
        instance = self.get_or_404(uid=instance_uid)
        self.session.delete(instance)
        self.session.commit()
