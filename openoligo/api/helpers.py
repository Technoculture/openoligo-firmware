"""
Convinience functions for code interaction with the database.
"""
from openoligo.api.models import SynthesisQueue, TaskStatus


async def update_task_status(task_id: int, status: TaskStatus):
    """Update the status of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(status=status)


async def set_task_status(task_id: int):
    """Set the status of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(status=TaskStatus.IN_PROGRESS)


async def set_log_file(task_id: int, log_file: str):
    """Set the log file of a synthesis task."""
    await SynthesisQueue.filter(id=task_id).update(log_file=log_file)


async def get_log_file(task_id: int) -> str:
    """Get the log file name of a synthesis task."""
    return await SynthesisQueue.get(id=task_id).values_list("log_file", flat=True)
