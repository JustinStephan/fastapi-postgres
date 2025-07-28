from fastapi import FastAPI
import models
from database import engine
from router import posts, cars

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(cars.router)

@app.get("/")
def read_root():
    return {"Hello world"}
