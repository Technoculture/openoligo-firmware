"""
Script to start the REST API server for OpenOligo.
"""
import logging
import uvicorn
from tortoise import Tortoise
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from api.models import Sequence, InstrumentStatus, Sequence_Model, InstrumentStatus_Model

#import openoligo as oo


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await Tortoise.init(
        db_url="sqlite://openoligo.db",
        modules={'models': ['api.models']}
    )
    await Tortoise.generate_schemas()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/sequence/")
async def add_sequence(sequence: str):
    seq = await Sequence.create(dna_sequence=sequence)
    return seq

@app.get("/sequence/{sequence_id}", response_model=Sequence_Model)
async def get_sequence(sequence_id: int):
    sequence = await Sequence.get_or_none(id=sequence_id)
    if sequence is None:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return sequence

@app.get("/instrument_status/{instrument_status_id}", response_model=InstrumentStatus_Model)
async def get_instrument_status(instrument_status_id: int):
    status = await InstrumentStatus.get_or_none(id=instrument_status_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Instrument status not found")
    return status

if __name__ == "__main__":
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)
