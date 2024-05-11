from fastapi import FastAPI

from .router import runs

app = FastAPI()

app.include_router(runs.router, tags=["接受数据推送"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
