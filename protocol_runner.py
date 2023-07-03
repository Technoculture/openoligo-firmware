import asyncio
import logging

from openoligo.api.helpers import (get_next_task, set_log_file,
                                   set_task_in_progress, update_task_status)
from openoligo.hal.instrument import Instrument
from openoligo.protocols.dna_synthesis import synthesize
from openoligo.seq import Seq
from openoligo.api.db import db_init, get_db_url
from openoligo.api.models import TaskStatus
from openoligo.hal.platform import __platform__

from openoligo.utils import log_config


async def main():
    await db_init(get_db_url(__platform__))
    inst = Instrument()

    while True:
        task = await get_next_task()
        if task is None:
            await asyncio.sleep(5)
            continue  # This will loop forever until a task is available
        await set_task_in_progress(task.id)
        await set_log_file(task.id, f"task_{task.id}.log")

        await synthesize(inst, seq=Seq(task.sequence))
        await update_task_status(task.id, TaskStatus.COMPLETE)


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.error("Keyboard interrupt detected, exiting...")
