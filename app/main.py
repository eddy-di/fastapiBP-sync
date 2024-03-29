from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def app_get():
    return {'info': "FastAPI Working"}
