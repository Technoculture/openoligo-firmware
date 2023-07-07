"""
Script to start the REST API server for OpenOligo.
"""
import uuid
from typing import Optional

import requests
import uvicorn
from fastapi import Body, FastAPI, HTTPException, status
from tortoise.exceptions import ValidationError

from openoligo.api.db import db_init, get_db_url

# from openoligo.api.models import Settings  # pylint: disable=unused-import
from openoligo.api.models import (  # EssentialReagentsModel,; SequencePartReagentsModel,
    AllReagents,
    EssentialReagents,
    SequencePartReagents,
    Settings,
    SettingsModel,
    SynthesisQueue,
    SynthesisQueueModel,
    TaskStatus,
    ValidSeq,
)
from openoligo.hal.platform import __platform__
from openoligo.seq import SeqCategory
from openoligo.utils.logger import OligoLogger

# from openoligo.api.helpers import get_settings


ol = OligoLogger(name="server", rotates=True)
logger = ol.get_logger()

rl = OligoLogger(rotates=True)
root_logger = rl.get_logger()

DESCRIPTION = """
OpenOligo API for the synthesis of oligonucleotides.

You can
* Request a new oligo synthesis task.
* Check the status of the sequences waiting to be synthesized.
* Read and Update the configuration and the staus of the instrument.

## SynthesisQueue

You will be able to:

* **Add a Sequence** to the Synthesis Queue.
* **Update the sequence and order of synthesis**.
* **Check the status** of a Sequence in the Queue.
* **Remove a Sequence** from the Queue.

## Instrument

You will be able to:

* **Read the configuration** of the instrument (_not implemented_).
* **Update the configuration** of the instrument (_not implemented_).
* **Read the status** of the instrument (_not implemented_).
* **Update the status** of the instrument (_not implemented_).
"""


app = FastAPI(
    title="OpenOligo API",
    summary="REST API for OpenOligo",
    description=DESCRIPTION,
    version="0.1.6",
    contact={
        "name": "Satyam Tiwary",
        "email": "satyam@technoculture.io",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


def get_public_ip() -> str:
    """Get the public IP address of the instrument."""
    try:
        return requests.get("https://api.ipify.org", timeout=1).text
    except requests.exceptions.Timeout:
        return ""


def get_mac() -> str:
    """Get the MAC address of the instrument."""
    return f"{uuid.getnode():012x}"


async def service_discovery(register: bool):
    """
    Register the service with the discovery service.

    Inform the service discovery node about the service,
    pass it our mac address, IP address and port
    """
    mac = get_mac()
    ip = get_public_ip()  # pylint: disable=invalid-name
    port = 9191

    print(f"MAC address: {mac}, IP address: {ip}, Service port: {port} -> {register}")

    # Call the service discovery node and register the service.
    # response = requests.post(
    #    "http://service_discovery_node_endpoint",
    #    json={
    #        "mac_address": mac,
    #        "ip_address": ip,
    #        "port": port,
    #    },
    # )

    # Check if the service was registered successfully.
    # if response.status_code == 200:
    #    print("Service registered successfully.")
    # else:
    #    print(f"Failed to register service. Status code: {response.status_code}")


@app.on_event("startup")
async def startup_event():
    """Startup event for the FastAPI server."""
    logger.info("Starting the API server...")  # pragma: no cover
    db_url = get_db_url(__platform__)  # pragma: no cover
    logger.info("Using database: '%s'", db_url)  # pragma: no cover
    await service_discovery(True)
    await db_init(db_url)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for the FastAPI server."""
    logger.info("Shutting down the API server...")


@app.get("/health", status_code=200, tags=["Utilities"])
def get_health_status():
    """Health check."""
    return {"status": "ok"}


@app.post("/queue", status_code=status.HTTP_201_CREATED, tags=["Synthesis Queue"])
async def add_a_task_to_synthesis_queue(
    sequence: str, category: SeqCategory = SeqCategory.DNA, rank: int = 0
):
    """Add a synthesis task to the synthesis task queue by providing a sequence and its category."""
    try:
        model = await SynthesisQueue.create(sequence=sequence, category=category, rank=rank)
        return model
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    finally:
        logger.info("Added sequence '%s' to the synthesis queue.", sequence)


@app.get(
    "/queue",
    response_model=list[SynthesisQueueModel],  # type: ignore
    status_code=status.HTTP_200_OK,
    tags=["Synthesis Queue"],
)
async def get_all_tasks_in_synthesis_queue(filter_by: Optional[TaskStatus] = None):
    """Get the current synthesis task queue."""
    tasks = SynthesisQueue.all().order_by("-rank", "-created_at")
    if filter_by:
        tasks = tasks.filter(status=filter)
    return await tasks


@app.delete("/queue", status_code=status.HTTP_200_OK, tags=["Synthesis Queue"])
async def clear_all_queued_tasks_in_task_queue():
    """Delete all tasks in the QUEUED state."""
    return await SynthesisQueue.filter(status=TaskStatus.QUEUED).delete()


@app.get("/queue/{task_id}", response_model=SynthesisQueueModel, tags=["Synthesis Queue"])
async def get_task_by_id(task_id: int):
    """Get a synthesis task from the queue."""
    task = await SynthesisQueue.get_or_none(id=task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sythesis task not found")
    return task


@app.put(
    "/queue/{task_id}",
    response_model=SynthesisQueueModel,
    status_code=status.HTTP_200_OK,
    tags=["Synthesis Queue"],
)
async def update_a_synthesis_task(
    task_id: int, sequence: Optional[str] = Body(None), rank: Optional[int] = Body(None)
):
    """Update a particular task in the queue."""
    task = await SynthesisQueue.get_or_none(id=task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sequence task not found")

    if task.status != TaskStatus.QUEUED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sequence task not in QUEUED state"
        )

    if sequence is None and rank is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Nothing to update. Provide sequence or rank.
(Sequence: {sequence}, Rank: {rank})""",
        )

    if sequence is not None:
        try:
            seq_validator = ValidSeq()
            seq_validator(sequence)
            task.sequence = sequence  # type: ignore
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if rank is not None and rank != task.rank:
        task.rank = rank  # type: ignore

    await task.save()

    return task


@app.delete("/queue/{task_id}", status_code=status.HTTP_200_OK, tags=["Synthesis Queue"])
async def delete_synthesis_task_by_id(task_id: int):
    """Delete a synthesis task from the queue."""
    task = await SynthesisQueue.get_or_none(id=task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sequence not found")

    await task.delete()

    return task


@app.get(
    "/about",
    tags=["Instrument"],
    response_model=list[SettingsModel],  # type: ignore
    status_code=200,
)
async def get_instrument_info():
    """Get information about the instrument."""
    settings = await Settings.first().values()
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instrument not configured with an Organisation",
        )
    return settings


@app.get(
    "/reagents",
    tags=["Instrument"],
    status_code=200,
    response_model=AllReagents,
)
async def get_all_reagents():
    """Get all reagents."""
    reactants = await EssentialReagents.all().values()
    components = await SequencePartReagents.all().values()
    return AllReagents(reactants=reactants, components=components)


def main():
    """Main function to start the server."""
    uvicorn.run(
        "openoligo.scripts.server:app", host="0.0.0.0", port=9191, reload=True
    )  # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
