from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBModel = declarative_base()
session_factory = sessionmaker()
Session = scoped_session(session_factory)
