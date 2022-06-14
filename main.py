import uvicorn as uvicorn

from fastapi import FastAPI, Depends, status, HTTPException, Query
from exceptions import BaseException
from service import get_address, create_address, delete_address, update_address, get_address_by_distance
from migration import get_db
from sqlalchemy.orm import Session
from logger import myLogger

logger = myLogger(__name__)

# initialize FastApi instance
app = FastAPI(title="Address REST API")


# define endpoint
@app.get("/")
def home():
    return {"addressbook": "address"}


@app.post("/create_address",
          description="Create a new address in address book",
          status_code=status.HTTP_201_CREATED
          )
async def create(name: str = Query(title="Name of the user"), latitude: float = Query(title="Latitude of the location",
                                                                                      description="Value should be in "
                                                                                                  "meter"),
                 longitude: float = Query(title="Longitude of the location", description="value should be in meter"),
                 zip_code: str = Query(None,
                                       description="Zip code Length "
                                                   "should not be less "
                                                   "then 4 and more "
                                                   "then 6",
                                       min_length=4,
                                       max_length=6),
                 db: Session = Depends(get_db)):
    """
     Create a new address object in database
    """
    try:
        logger.info('creating a address object in DB')
        address = create_address(db=db, name=name, zip_code=zip_code, latitude=latitude, longitude=longitude)
        # return object created
        return {"address": address}
    except BaseException as cie:
        raise HTTPException(**cie.__dict__)


@app.get("/get_address/{address_id}/",
         description='Get a single address by its unique ID',
         status_code=status.HTTP_200_OK)  # address_id is a path parameter
async def get(address_id: int, db: Session = Depends(get_db)):
    """
         Get an address object from database
    """
    try:
        logger.info('getting an address object from DB')
        address = get_address(db=db, address_id=address_id)
        return address
    except BaseException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/update_address/{id}/",
         description='Update a single address by its unique id'
         )  # address_id is a path parameter
async def update(address_id: int, name: str = Query(title="Name of the user"),
                 latitude: float = Query(title="Latitude of the location", description="value should be in meter"),
                 longitude: float = Query(title="Longitude of the location", description="value should be in meter"),
                 zip_code: str = Query(None,
                                       description="Zip code Length "
                                                   "should not be less "
                                                   "then 4 and more "
                                                   "then 6 ",
                                       min_length=4,
                                       max_length=6),
                 db: Session = Depends(get_db)):
    """
             Updating an address object in database
    """
    try:
        # get address object from database
        db_address = get_address(db=db, address_id=address_id)
        # check if Address object exists
        if db_address:
            logger.info('updating an address object attribute in DB')
            updated_address = update_address(db=db, address_id=address_id, name=name, zip_code=zip_code,
                                             latitude=latitude,
                                             longitude=longitude)
            return updated_address
        else:
            return {"error": f"Address with id {id} does not exist"}
    except BaseException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/delete_address/{id}/",
            description='delete a single address by its unique id')  # address_id is a path parameter
async def delete(address_id: int, db: Session = Depends(get_db)):
    """
                 Deleting an address object in database
    """
    try:
        # get address object from database
        db_friend = get_address(db=db, address_id=address_id)
        # check if address object exists
        if db_friend:
            return delete_address(db=db, address_id=address_id)
        else:
            return {"error": f"Address with id {id} does not exist"}
    except BaseException as cie:
        raise HTTPException(**cie.__dict__)


@app.get("/get_addresses/{distance}/",
         description='Get all address within a given distance',
         status_code=status.HTTP_200_OK)  # address_id is a path parameter
async def get_addresses(distance: float, latitude: float, longitude: float, db: Session = Depends(get_db)):
    """
         Get all address within a given distance from database
    """
    try:
        addresses = get_address_by_distance(db=db, distance=distance, latitude=latitude, longitude=longitude)
        return addresses
    except BaseException as cie:
        raise HTTPException(**cie.__dict__)


if __name__ == '__main__':
    # create_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
