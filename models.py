from sqlalchemy import Column, String, Integer, Float
from migration import Base, engine


# model/table
class Address(Base):
    __tablename__ = 'address'

    # fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True, nullable=False)  # unique=True
    zip_code = Column(String(6), index=True, nullable=False, default=None)  # unique=True
    latitude = Column(Float, index=True, nullable=False)  # unique=True
    longitude = Column(Float, index=True, nullable=False)  # unique=True


# create the database tables on app startup or reload
Base.metadata.create_all(bind=engine)
