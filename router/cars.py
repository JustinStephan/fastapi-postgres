from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import models
import schemas
import csv

router = APIRouter(
    prefix='/cars',
    tags=['tags']
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Car])
def get_cars(limit: int = 10, db: Session = Depends(get_db)):
    print('test')
    cars = db.query(models.Car).limit(limit)
    return cars

@router.post('/import-csv', status_code=status.HTTP_202_ACCEPTED)
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print('test')
    try:
        raw = await file.read()
        contents = raw.decode("utf-8").splitlines()
        reader = csv.DictReader(contents)

        cars = []
        for row in reader:
            parsed = schemas.Car(**row)
            cars.append(models.Car(**parsed.model_dump()))
        
        db.bulk_save_objects(cars)
        db.commit()
        return {"filename": file.filename, "content_length": len(cars)}
    except Exception as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail="Invalid request data")
