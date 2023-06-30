"""
Script to start the REST API server for OpenOligo.
"""
import logging
import uvicorn
from fastapi import FastAPI


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
   uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
