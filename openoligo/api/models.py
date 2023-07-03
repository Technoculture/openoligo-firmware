"""
Tortoise ORM Models for the OpenOligo API
"""
import re
from enum import Enum

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError
from tortoise.models import Model
from tortoise.validators import MinLengthValidator, RegexValidator, Validator

from openoligo.seq import Seq, SeqCategory


class TaskStatus(str, Enum):
    """Status of a synthesis task."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"


class ValidSeq(Validator):  # pylint: disable=too-few-public-methods
    """Validate that the value is a valid NA sequence"""

    def __call__(self, value: str) -> None:
        """Validate the value."""
        try:
            Seq(value)
            assert len(value) >= 3, "Sequence must be at least 3 bases long"
            assert len(value) <= 100, "Sequence must be at most 100 bases long"
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        except AssertionError as exc:
            raise ValidationError(str(exc)) from exc


class SynthesisQueue(Model):
    """A synthesis task in the queue."""

    id = fields.IntField(pk=True, autoincrement=True, description="Synthesis ID")

    sequence = fields.TextField(
        validators=[ValidSeq()],
        description="Sequence of the Nucliec Acid to synthesize",
    )
    category = fields.CharEnumField(
        SeqCategory,
        default=SeqCategory.DNA,
        description="Category of the sequence, eg. DNA, RNA, or MIXED",
    )
    status = fields.CharEnumField(TaskStatus, default=TaskStatus.QUEUED)

    rank = fields.IntField(
        default=0,
        description="""Rank of the synthesis task in the queue.
        0 is for chronologically first.
        Other numbers are prioritised over 0 in the increasing order""",
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    started_at = fields.DatetimeField(null=True)
    completed_at = fields.DatetimeField(null=True)

    log_file = fields.TextField(
        null=True,
        validate=[MinLengthValidator(5), RegexValidator(r"\.log$", flags=re.I)],
    )

    class PydanticMeta:  # pylint: disable=too-few-public-methods
        """Pydantic configuration"""

        exclude = ["log_file"]
        ordering = ["-rank", "-created_at"]


SynthesisQueueModel = pydantic_model_creator(SynthesisQueue, name="SynthesisQueue")
