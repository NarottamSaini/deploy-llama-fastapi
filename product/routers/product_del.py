from fastapi import APIRouter
from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from fastapi.params import Depends

from ..import schemas
from ..import models
# from .import login
from .signin import get_current_user
# from product.routers.login import get_current_user
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(tags=['Products'],
                   prefix="/product")


## response_model : parameter is used to limit the field/values to be displayed in api response. Only thosefield defined in DisplayProduct class will be dispalyed
## List[schemas.DisplayProduct] : List required as output will be multiple records
@router.get('/', response_model=List[schemas.DisplayProduct])
def product(db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

## response_model : parameter is used to limit the field/values to be displayed in api response. Only thosefield defined in DisplayProduct class will be dispalyed
@router.get('/{id}', response_model=schemas.DisplayProduct)
def product(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.index == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not Found')
    
    return product


@router.delete('/{id}')
def delete(id, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.index == id).delete(synchronize_session=False)
    db.commit()
    return "Record deleted successfully"

@router.put('/product_update/{id}')
def product_update(id, request:schemas.Product, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.index == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return "Product updated successfully"
    
## status_code : parameter for adding appropriate status to the response rather than only 200 as response
@router.post('/', status_code=status.HTTP_201_CREATED)
def add(request:schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description = request.description, price = request.price,
                                 seller_id = 1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request