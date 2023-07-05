"""
Convinience functions for code interaction with the database.
"""
from datetime import datetime
from typing import Optional

from openoligo.api.models import SynthesisQueue, TaskStatus


async def update_task_status(task_id: int, status: TaskStatus):
    """Update the status of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(status=status)


async def set_started_now(task_id: int):
    """Set the started_at timestamp of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(started_at=datetime.now())


async def set_completed_now(task_id: int):
    """Set the completed_at timestamp of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(completed_at=datetime.now())


async def set_failed_now(task_id: int):
    """Set the completed_at timestamp of a synthesis task."""
    await update_task_status(task_id, TaskStatus.FAILED)


async def set_task_in_progress(task_id: int):
    """Set the status of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(status=TaskStatus.IN_PROGRESS)


async def set_log_file(task_id: int, log_file: str):
    """Set the log file of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(log_file=log_file)


async def get_log_file(task_id: int) -> str:
    """Get the log file name of a synthesis task."""
    return await SynthesisQueue.get(id=task_id).values_list("log_file", flat=True)


async def get_next_task() -> Optional[SynthesisQueue]:
    """Get the next synthesis task."""
    return (
        await SynthesisQueue.filter(status=TaskStatus.QUEUED)
        .order_by("-rank", "created_at")
        .first()
    )
