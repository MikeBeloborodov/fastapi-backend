from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
from .schemas import *


SQLALCHEMY_DATABASE_URL = (f"postgresql://"
                            f"{settings.database_username}:"
                            f"{settings.database_password}@"
                            f"{settings.database_hostname}/"
                            f"{settings.database_name}")


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# db session for sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()