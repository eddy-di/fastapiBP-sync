from fastapi import FastAPI

from app.auth.routers import auth

app = FastAPI()


@app.get('/')  # type: ignore
def app_get():
    return {'info': 'FastAPI Working'}


app.include_router(auth)
