import uvicorn

from fastapi import FastAPI

from p2.router import execution


app = FastAPI()
app.include_router(execution.router, prefix="/p2")



@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
