from fastapi import FastAPI

from server import models
from server.database import engine
import auth
app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.route)

@app.get("/")
def read_root():
    return {"status": "up", 'database-connection': 'established'}
