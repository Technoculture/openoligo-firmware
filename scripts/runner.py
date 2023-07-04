"""
Runner Script.

This script runs the infinite loop that checks for new tasks and executes them.
"""
import os
import anyio

from openoligo.api.db import db_init, get_db_url
from openoligo.api.helpers import (get_next_task, set_log_file,
                                   set_task_in_progress, update_task_status,
                                   set_started_now, set_completed_now)
from openoligo.api.models import TaskStatus
from openoligo.hal.instrument import Instrument
from openoligo.hal.platform import __platform__
from openoligo.protocols.dna_synthesis import synthesize
from openoligo.seq import Seq
from openoligo.utils.logger import OligoLogger

ol = OligoLogger(name="runner", rotates=True)
logger = ol.get_logger()


rl = OligoLogger(rotates=False)
root_logger = rl.get_logger()


async def worker():
    """
    This is the actual worker.

    Essentially, it will loop forever, checking for new tasks in the database and executing them.
    """
    logger.info("OpenOligo Runner: Worker process started")
    await db_init(get_db_url(__platform__))
    inst = Instrument()

    while True:
        task = await get_next_task()
        if task is None:
            await anyio.sleep(5)
            continue  # This will loop forever until a task is available

        logger.info(f"Got new task: {task}")
        await set_task_in_progress(task.id)
        logger.info(f"Task {task.id} set to in progress")

        # Set the log file for this task
        name = f"task_{task.id}"
        await set_log_file(task.id, f"{name}.log")
        rl.change_log_file(name)

        await set_started_now(task.id)
        await update_task_status(task.id, TaskStatus.IN_PROGRESS)
        logger.info(f"Starting task {task.id}")

        # Execute the task
        await synthesize(inst, seq=Seq(task.sequence))

        await set_completed_now(task.id)
        await update_task_status(task.id, TaskStatus.COMPLETE)
        logger.info(f"Task {task.id} complete")


def main():
    """
    Main entry point of the runner.
    """
    logger.info("OpenOligo Runner: Starting")

    try:
        anyio.run(worker)
    except KeyboardInterrupt:
        logger.error("Keyboard interrupt detected, shutting down")
        os._exit(0)  # A hard exit is required to kill the logging thread


if __name__ == "__main__":
    main()
    logger.error("OpenOligo Runner: Natural exit, SHOULD NEVER HAPPEN.")
