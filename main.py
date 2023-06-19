import uvicorn
from fastapi import FastAPI

from api.login_router import login_router
from api.user_router import user_router

app = FastAPI(title="oxford university")


app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(login_router, prefix="/login", tags=["Login"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
