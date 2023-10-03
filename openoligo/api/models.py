"""
Tortoise ORM Models for the OpenOligo API
"""
import re
from dataclasses import dataclass
from enum import Enum

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError
from tortoise.models import Model
from tortoise.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
    Validator,
)

from openoligo.seq import Seq


class TaskStatus(str, Enum):
    """Status of a synthesis task."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"


class ReactantType(str, Enum):
    """Type of Sequence Part."""

    TERMINAL3 = "terminal3"
    TERMINAL5 = "terminal5"
    NUCLEOTIDE = "nucleotide"
    MODIFIED_NUCLEOTIDE = "modified_nucleotide"
    REACTANT = "reactant"


class InstrumentHealth(str, Enum):
    """Instrument health status"""

    OPERATIONAL = "Operational"
    DEGRADED = "Degraded"
    MAINTAINANCE = "Maintenance"
    OFFLINE = "Offline"


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


class Backbone(str, Enum):
    """Backbone of a sequence."""

    PO = "PO"
    PS = "PS"


class Nucleobase(str, Enum):
    """Nucleobase of a nucleotide."""

    A = "Adenine"
    C = "Cytosine"
    G = "Guanine"
    T = "Thymine"
    U = "Uracil"
    I = "Inosine"  # noqa: E741


@dataclass
class NucleobaseInfo:
    """Information regarding a particular nucleotide"""

    name: str
    is_terminal: bool = False


NucleobasesInfo: dict[Nucleobase, NucleobaseInfo] = {
    Nucleobase.A: NucleobaseInfo(name="Adenine"),
    Nucleobase.T: NucleobaseInfo(name="Thymine"),
    Nucleobase.G: NucleobaseInfo(name="Guanine"),
    Nucleobase.C: NucleobaseInfo(name="Cytosine"),
    Nucleobase.I: NucleobaseInfo(name="Inosine"),
}


class Sugar(str, Enum):
    """Sugar of a nucleotide."""

    OH = "OH"
    H = "H"
    MOE = "MOE"
    OMOE = "OMOE"
    F = "F"


class SolidSupport(str, Enum):
    """Solid support of a nucleotide."""

    UNIVERSAL = "Universal"
    GALNAC = "GalNAc"


class Nucleotide(Model):
    """Nucleotide Model"""

    id = fields.IntField(pk=True, autoincrement=True, description="The ID of the nucleotide")
    accronym = fields.CharField(
        max_length=10, unique=True, description="The accronym of the nucleotide"
    )
    backbone = fields.CharEnumField(
        Backbone, default=Backbone.PO, description="The backbone of the nucleotide"
    )
    sugar = fields.CharEnumField(Sugar, default=Sugar.H, description="Sugar of the nucleotide")
    base = fields.CharEnumField(Nucleobase, description="The nucleobase of the nucleotide")
    quantity = fields.IntField(
        default=0, description="The quantity of the nucleotide in the inventory"
    )


class SynthesisTask(Model):
    """A synthesis task in the queue."""

    id = fields.IntField(pk=True, autoincrement=True, description="Synthesis ID")

    sequence = fields.TextField(
        validators=[ValidSeq()],
        description="Sequence of the Nucliec Acid to synthesize",
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


class Settings(Model):
    """Settings for this particular instrument."""

    id = fields.IntField(pk=True, autoincrement=True, description="Settings ID")
    org_uuid = fields.TextField(
        description="UUID of the organisation", validators=[MinLengthValidator(8)]
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class PydanticMeta:  # pylint: disable=too-few-public-methods
        """Pydantic configuration"""

        ordering = ["-created_at"]
        exclude = ["id"]


class Reactant(Model):
    """A part of a sequence, such as nucleotides, or terminal modifications."""

    accronym = fields.CharField(
        pk=True, max_length=10, description="Accronym of the reagent", unique=True
    )
    name = fields.TextField(description="Name of the part")
    volume = fields.FloatField(
        description="Volume of the part in mL",
        validators=[MinValueValidator(0.0), MaxValueValidator(1000.0)],
    )
    current_volume = fields.FloatField(
        description="Volume of the reagents estimated to be available currently in mL",
        validators=[MinValueValidator(0.0), MaxValueValidator(1000.0)],
    )
    reactant_type = fields.CharEnumField(ReactantType, description="Type of sequence part")
    inserted_at = fields.DatetimeField(
        auto_now_add=True, description="When was this reagent inserted?"
    )
    updated_at = fields.DatetimeField(auto_now_add=True, description="Last time this part was used")

    class PydanticMeta:  # pylint: disable=too-few-public-methods
        """Pydantic configuration"""

        ordering = ["current_volume", "-updated_at", "-inserted_at"]


SynthesisTaskModel = pydantic_model_creator(SynthesisTask, name="SynthesisTask")

SettingsModel = pydantic_model_creator(Settings, name="Settings")

ReactantModel = pydantic_model_creator(Reactant, name="ReactantModel")
