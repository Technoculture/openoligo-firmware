"""
Convinience functions for code interaction with the database.
"""
from openoligo.api.models import TaskQueue, TaskStatus


def update_task_status(task_id: int, status: TaskStatus):
    """
    Update the status of a task.
    """
    TaskQueue.filter(id=task_id).update(status=status)


def set_active_task(task_id: int):
    """
    Set the status of a task.
    """
    TaskQueue.filter(id=task_id).update(status=TaskStatus.IN_PROGRESS)


def set_concluding_remark(task_id: int, remark: str):
    """
    Set the concluding remark of a task.
    """
    TaskQueue.filter(id=task_id).update(concluding_remark=remark)


def set_log_file(task_id: int, log_file: str):
    """
    Set the log file of a task.
    """
    TaskQueue.filter(id=task_id).update(log_file=log_file)


def get_log_file(task_id: int) -> str:
    """
    Get the log file name of a task.
    """
    return TaskQueue.get(id=task_id).log_file
