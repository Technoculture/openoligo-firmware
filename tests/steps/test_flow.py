import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from openoligo.steps.flow import (
    dry,
    dry_all,
    send_to_prod,
    send_to_waste_rxn,
    solvent_wash,
    solvent_wash_all,
)
from openoligo.steps.types import FlowBranch


def test_send_to_prod():
    instrument = MagicMock()
    src = "test_src"
    asyncio.run(send_to_prod(instrument, src))
    instrument.all_except.assert_called_once_with([src, "prod", "branch", "rxn_out"])


def test_send_to_waste_rxn():
    instrument = MagicMock()
    src = "test_src"
    asyncio.run(send_to_waste_rxn(instrument, src))
    instrument.all_except.assert_called_once_with([src, "branch", "rxn_out", "waste_rxn"])


def test_solvent_wash_reagents():
    instrument = MagicMock()
    branch_reagents = FlowBranch.REAGENTS
    duration = 10

    asyncio.run(solvent_wash(instrument, branch_reagents, duration))
    instrument.all_except.assert_called_once_with(["sol", "waste"])


def test_solvent_wash_reaction():
    instrument = MagicMock()
    branch_reaction = FlowBranch.REACTION
    duration = 10

    asyncio.run(solvent_wash(instrument, branch_reaction, duration))
    instrument.all_except.assert_called_once_with(["sol", "rxn_out", "branch", "waste_rxn"])


def test_solvent_wash_all():
    instrument = MagicMock()
    solvent_wash = AsyncMock()

    with patch("openoligo.steps.flow.solvent_wash", new=solvent_wash):
        asyncio.run(solvent_wash_all(instrument))

    solvent_wash.assert_any_call(instrument, FlowBranch.REACTION)
    solvent_wash.assert_any_call(instrument, FlowBranch.REAGENTS)


def test_dry_reagents():
    instrument = MagicMock()
    branch_reagents = FlowBranch.REAGENTS

    asyncio.run(dry(instrument, branch_reagents))
    instrument.all_except.assert_called_once_with(["gas", "waste"])


def test_dry_reactions():
    instrument = MagicMock()
    branch_reaction = FlowBranch.REACTION

    asyncio.run(dry(instrument, branch_reaction))
    instrument.all_except.assert_called_once_with(["gas", "rxn_out", "branch", "waste_rxn"])


def test_dry_all():
    instrument = MagicMock()
    dry = AsyncMock()

    with patch("openoligo.steps.flow.dry", new=dry):
        asyncio.run(dry_all(instrument))

    dry.assert_any_call(instrument, FlowBranch.REACTION)
    dry.assert_any_call(instrument, FlowBranch.REAGENTS)
