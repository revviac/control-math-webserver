from fastapi import FastAPI
from src.routers import control
import uvicorn
import colorama

# Initialize colorama to prevent buggy log output
colorama.init()


app = FastAPI()


app.include_router(control.router, prefix="/control", tags=["control"])


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
