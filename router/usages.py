from fastapi import APIRouter, UploadFile, HTTPException, Depends, File
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import usage_model
import usage_schema
import csv

router = APIRouter(
    prefix = '/usages'
)



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[usage_schema.UsageCreate])
def get_usages(location: str | None = None , year: int | None = None , db: Session = Depends(get_db)):
    usages = db.query(usage_model.Usage)
    if location is not None:
        usages = usages.filter(usage_model.Usage.location == location)

    if year is not None:
        usages = usages.filter(usage_model.Usage.year == year)

    return usages.all()


@router.post('/import-csv', status_code=status.HTTP_202_ACCEPTED)
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print('test')
    try:
        raw = await file.read()
        contents = raw.decode("utf-8").splitlines()
        reader = csv.DictReader(contents)

        usages = []
        for row in reader:
            parsed = usage_schema.UsageCreate(**row)
            usages.append(usage_model.Usage(**parsed.model_dump()))
        
        db.bulk_save_objects(usages)
        db.commit()
        return {"filename": file.filename, "content_length": len(usages)}
    except Exception as e:
        print(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail="Invalid request data")