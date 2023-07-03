import pytest
from tortoise.exceptions import ValidationError

from openoligo.api.models import SynthesisQueue, TaskStatus
from openoligo.seq import SeqCategory


@pytest.mark.asyncio
async def test_create_synthesis_queue(db):
    synthesis_queue = await SynthesisQueue.create(
        sequence="ATCG", category=SeqCategory.DNA, status=TaskStatus.QUEUED, rank=0
    )

    assert synthesis_queue.id == 1
    assert synthesis_queue.sequence == "ATCG"
    assert synthesis_queue.category == SeqCategory.DNA
    assert synthesis_queue.status == TaskStatus.QUEUED
    assert synthesis_queue.rank == 0


@pytest.mark.asyncio
async def test_synthesis_queue_validation(db):
    with pytest.raises(ValidationError):
        await SynthesisQueue.create(
            sequence="ATXG",  # Invalid Sequence
            category=SeqCategory.DNA,
            status=TaskStatus.QUEUED,
            rank=0,
        )


@pytest.mark.asyncio
async def test_update_synthesis_queue_status(db):
    synthesis_queue = await SynthesisQueue.create(
        sequence="ATCG", category=SeqCategory.DNA, status=TaskStatus.QUEUED, rank=0
    )

    await synthesis_queue.all().update(status=TaskStatus.IN_PROGRESS)
    synthesis_queue_updated = await SynthesisQueue.get(id=synthesis_queue.id)

    assert synthesis_queue_updated.status == TaskStatus.IN_PROGRESS
