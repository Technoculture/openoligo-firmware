from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Sequence(Model):
    id = fields.IntField(pk=True)
    dna_sequence = fields.TextField()


class InstrumentStatus(Model):
    id = fields.IntField(pk=True)
    reagents_loaded = fields.JSONField()
    queue_status = fields.CharField(max_length=200)
    max_queue_size = fields.IntField()


Sequence_Model = pydantic_model_creator(Sequence, name="Sequence")
InstrumentStatus_Model = pydantic_model_creator(InstrumentStatus, name="InstrumentStatus")
