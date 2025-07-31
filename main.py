from fastapi import FastAPI
import models
import usage_model
from database import engine
from router import posts, cars, usages

models.Base.metadata.create_all(bind=engine)
usage_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(cars.router)
app.include_router(usages.router)

@app.get("/")
def read_root():
    return {"Hello world"}
