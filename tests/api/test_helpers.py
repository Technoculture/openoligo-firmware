import pytest

from openoligo.api.helpers import (
    get_log_file,
    set_log_file,
    set_task_in_progress,
    update_task_status,
)
from openoligo.api.models import SynthesisTask, TaskStatus
from openoligo.seq import SeqCategory


@pytest.mark.asyncio
async def test_update_task_status(db):
    synthesis_queue = await SynthesisTask.create(
        sequence="ATCG", category=SeqCategory.DNA, status=TaskStatus.QUEUED, rank=0
    )
    await update_task_status(synthesis_queue.id, TaskStatus.IN_PROGRESS)
    synthesis_queue_updated = await SynthesisTask.get(id=synthesis_queue.id)
    assert synthesis_queue_updated.status == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_set_active_task(db):
    synthesis_queue = await SynthesisTask.create(
        sequence="ATCG", category=SeqCategory.DNA, status=TaskStatus.QUEUED, rank=0
    )
    await set_task_in_progress(synthesis_queue.id)
    synthesis_queue_updated = await SynthesisTask.get(id=synthesis_queue.id)
    assert synthesis_queue_updated.status == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_set_log_file(db):
    synthesis_queue = await SynthesisTask.create(
        sequence="ATCG", category=SeqCategory.DNA, status=TaskStatus.QUEUED, rank=0
    )
    await set_log_file(synthesis_queue.id, "Test log")
    synthesis_queue_updated = await SynthesisTask.get(id=synthesis_queue.id)
    assert synthesis_queue_updated.log_file == "Test log"


@pytest.mark.asyncio
async def test_get_log_file(db):
    synthesis_queue = await SynthesisTask.create(
        sequence="ATCG",
        category=SeqCategory.DNA,
        status=TaskStatus.QUEUED,
        rank=0,
        log_file="Test log",
    )
    log_file = await get_log_file(synthesis_queue.id)
    assert log_file == "Test log"
