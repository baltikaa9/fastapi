import uvicorn
from fastapi import FastAPI

from api.routers import user_router

app = FastAPI(title="oxford university")


app.include_router(user_router, prefix="/user", tags=["User"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
