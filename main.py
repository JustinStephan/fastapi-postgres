from fastapi import FastAPI
import models
from database import engine
from router import posts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"Hello world"}
