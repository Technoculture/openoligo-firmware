"""
Runner Script.

This script runs the infinite loop that checks for new tasks and executes them.
"""
import os

import anyio

from openoligo.api.db import db_init, get_db_url
from openoligo.api.helpers import (get_next_task, set_log_file,
                                   set_task_in_progress, update_task_status)
from openoligo.api.models import TaskStatus
from openoligo.hal.instrument import Instrument
from openoligo.hal.platform import __platform__
from openoligo.protocols.dna_synthesis import synthesize
from openoligo.seq import Seq
from openoligo.utils.logger import configure_logger

logger = configure_logger("runner.log", rotates=True)


async def worker():
    """
    This is the actual worker.

    Essentially, it will loop forever, checking for new tasks in the database and executing them.
    """
    await db_init(get_db_url(__platform__))
    inst = Instrument()

    while True:
        task = await get_next_task()
        if task is None:
            await anyio.sleep(5)
            continue  # This will loop forever until a task is available
        await set_task_in_progress(task.id)
        await set_log_file(task.id, f"task_{task.id}.log")

        await synthesize(inst, seq=Seq(task.sequence))
        await update_task_status(task.id, TaskStatus.COMPLETE)


def main():
    """
    Main entry point of the runner.
    """
    logger.info("Starting openoligo runner")
    try:
        anyio.run(worker)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected, shutting down")
        os._exit(0)  # A hard exit is required to kill the logging thread


if __name__ == "__main__":
    main()
