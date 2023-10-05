"""
Convinience functions for code interaction with the database.
"""
from datetime import datetime
from typing import Optional

from openoligo.api.models import Reactant, Settings, SynthesisTask, TaskStatus


async def update_task_status(task_id: int, status: TaskStatus):
    """Update the status of a synthesis task."""
    await SynthesisTask.filter(id=task_id).update(status=status)


async def set_started_now(task_id: int):
    """Set the started_at timestamp of a synthesis task."""
    await SynthesisTask.filter(id=task_id).update(started_at=datetime.now())


async def set_completed_now(task_id: int):
    """Set the completed_at timestamp of a synthesis task."""
    await SynthesisTask.filter(id=task_id).update(completed_at=datetime.now())


async def set_failed_now(task_id: int):
    """Set the completed_at timestamp of a synthesis task."""
    await update_task_status(task_id, TaskStatus.SYNTHESIS_FAILED)


async def set_task_in_progress(task_id: int):
    """Set the status of a synthesis task."""
    await SynthesisTask.filter(id=task_id).update(status=TaskStatus.SYNTHESIS_IN_PROGRESS)


async def set_log_file(task_id: int, log_file: str):
    """Set the log file of a synthesis task."""
    await SynthesisTask.filter(id=task_id).update(log_file=log_file)


async def get_log_file(task_id: int) -> str:
    """Get the log file name of a synthesis task."""
    return await SynthesisTask.get(id=task_id).values_list("log_file", flat=True)  # type: ignore


async def set_org_id(org_id: str) -> None:
    """Set the organisation ID."""
    await Settings.create(org_id=org_id)


async def get_instrument_settings() -> Optional[Settings]:
    """Get the instrument settings."""
    return await Settings.first()


async def get_settings() -> Optional[list[Settings]]:
    """Get the organisation ID."""
    settings = await Settings.first().values()
    return [Settings(**setting) for setting in settings] if settings else None


async def update_reactant_used(accronym: str, volume: float) -> None:
    """Reduce the volume of a reagent by the given amount."""
    assert volume >= 0, "Volume must be positive"
    reagent = await Reactant.get(accronym=accronym).values("current_volume")
    current_volume = reagent[0]["current_volume"]
    await Reactant.filter(accronym=accronym).update(current_volume=current_volume - volume)


async def get_all_reactants() -> list[Reactant]:
    """Get all reactants."""
    return await Reactant.all()


async def create_new_reactant(name: str, accronym: str, volume: float) -> None:
    """Create a new reactants."""
    await Reactant.create(name=name, accronym=accronym, volume=volume, current_volume=volume)


async def get_next_task() -> Optional[SynthesisTask]:
    """Get the next synthesis task."""
    return (
        await SynthesisTask.filter(status=TaskStatus.WAITING_IN_QUEUE)
        .order_by("-rank", "created_at")
        .first()
    )
