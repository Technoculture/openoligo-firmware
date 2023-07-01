"""
Script to start the REST API server for OpenOligo.
"""
import logging
import uvicorn
from tortoise import Tortoise
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from tortoise.exceptions import ValidationError

from api.models import (
    TaskQueue,
    TaskQueueModel,
)

from openoligo.hal.platform import Platform, __platform__


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    if not __platform__:
        raise RuntimeError("No platform detected")

    db_url = "sqlite://openoligo.db"
    if __platform__ == Platform.RPI or __platform__ == Platform.BB:
        db_url = "sqlite:////var/log/openoligo.db"
    await Tortoise.init(db_url=db_url, modules={"models": ["api.models"]})
    await Tortoise.generate_schemas()


@app.get("/health")
def root():
    return {"status": "ok"}


@app.post("/queue")
async def add_to_queue(task: TaskQueueModel):
    try:
        await TaskQueue.create(sequence=task.sequence, category=task.category)
        return Response(status_code=201)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/queue/", response_model=list[TaskQueueModel])
async def get_task_queue():
    return await TaskQueue.all().limit(100)


@app.get("/queue/{task_id}", response_model=TaskQueueModel)
async def get_task(task_id: int):
    task = await TaskQueue.get_or_none(id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/queue/{task_id}", status_code=200)
async def update_task(task_id: int, sequence: str):
    task = await TaskQueue.get_or_none(id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Sequence not found")

    if task.status != "queued":
        raise HTTPException(status_code=400, detail="Task is not queued")

    task.sequence = sequence
    await task.save()

    return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="127.0.0.1", port=9191, reload=True)
