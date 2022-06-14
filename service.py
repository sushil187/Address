import math

from sqlalchemy.orm import Session

from fastapi import HTTPException

from models import Address

from logger import myLogger

logger = myLogger(__name__)


def create_address(db: Session, name: str, zip_code: str, latitude: float, longitude: float):
    """
    function to create an address model object
    """
    try:
        # creating an  address instance
        logger.info('creating a  address instance')
        new_address = Address(name=name, zip_code=zip_code, latitude=latitude, longitude=longitude)
        # place object in the database session
        logger.info('place object in the database session')
        db.add(new_address)
        # commit instance to the database
        logger.info('commit instance to the database')
        db.commit()
        # refresh the attributes of the given instance
        logger.info('refresh the attributes of the given instance')
        db.refresh(new_address)
        return new_address
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(**ex.__dict__)


def get_address(db: Session, address_id: int):
    """
    get the first record with a given id, if no such record exists, will return null
    """
    try:
        logger.info('getting the first record with a given id')
        db_address = db.query(Address).filter(Address.id == address_id).first()
        return db_address
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(**ex.__dict__)


def update_address(db: Session, address_id: int, name: str, zip_code: str, latitude: float, longitude: float):
    """
    Update an Address object's attributes
    """
    try:
        logger.info('setting an Address object attributes')
        db_address = get_address(db=db, address_id=address_id)
        db_address.name = name
        db_address.zip_code = zip_code
        db_address.latitude = latitude
        db_address.longitude = longitude
        logger.info('commit instance to the database')
        db.commit()
        db.refresh(db_address)  # refresh the attribute of the given instance
        return db_address
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(**ex.__dict__)


def delete_address(db: Session, address_id: int):
    """
    Delete a Address object
    """
    try:
        logger.info('getting an instance from the DB')
        db_address = get_address(db=db, address_id=address_id)
        db.delete(db_address)
        db.commit()  # save changes to db
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(**ex.__dict__)


def calculate_new_position(latitude: float, longitude: float, distance: float):
    # number of km per degree = 111.32 km in google maps
    # 1 m in degree = 1 / 1000 * 111.32
    coef = distance * 0.0000089

    # Calculating new latitude and longitude value
    new_lat = latitude + coef
    new_long = longitude + coef / math.cos(latitude * 0.018)

    return new_lat, new_long


def get_address_by_distance(db: Session, distance: float, latitude: float, longitude: float):
    """
     function for getting all address within a given distance
    """
    try:
        logger.info('Finding new latitude and longitude coordinates')
        new_lat, new_long = calculate_new_position(latitude, longitude, distance)
        min_lat, max_lat, min_long, max_long = min(latitude, new_lat), max(latitude, new_lat), min(longitude, new_long), \
                                               max(longitude, new_long)
        logger.info('Filtering out all addresses which location coordinates lie in range')
        db_addresses = db.query(Address).filter(Address.latitude >= min_lat, Address.latitude <= max_lat,
                                                Address.longitude >= min_long, Address.longitude <= max_long).all()
        return db_addresses
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(**ex.__dict__)
