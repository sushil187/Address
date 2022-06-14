from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import myLogger

logger = myLogger(__name__)

# define sqlite connection url
SQLALCHEMY_DATABASE_URL = "sqlite:///./address_api.db"

# create new engine instance 
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False},)

# create sessionmaker 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    logger.info('Creating a DB Connection')
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info('Closing a DB Connection')
        db.close()
