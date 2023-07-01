import re
from enum import Enum

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.validators import Validator, MinLengthValidator, RegexValidator
from tortoise.exceptions import ValidationError

from openoligo.seq import Seq, SeqCategory


class TaskStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    ERROR = "error"


class ValidSeq(Validator):
    """
    Validate that the value is a valid NA sequence
    """

    def __call__(self, value: str):
        try:
            Seq(value)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc


class TaskQueue(Model):
    id = fields.IntField(pk=True)
    sequence = fields.TextField(validators=[ValidSeq()])
    category = fields.CharEnumField(SeqCategory)
    status = fields.CharEnumField(TaskStatus, default=TaskStatus.QUEUED)
    concluding_remark = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    started_at = fields.DatetimeField(null=True)
    completed_at = fields.DatetimeField(null=True)

    log_file = fields.TextField(null=True, validate=[
        MinLengthValidator(5), 
        RegexValidator(r"\.log$", flags=re.I)
    ])


TaskQueueModel = pydantic_model_creator(TaskQueue, name="TaskQueue")
