from fastapi import FastAPI
from routes import repositories

app = FastAPI()

app.include_router(repositories.router, prefix="/repositories", tags=["Repositories"])
