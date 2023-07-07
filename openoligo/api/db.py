"""
Conviniences for initializing the database.
"""
import os

from tortoise import Tortoise

from openoligo.hal.platform import Platform

tmp_dir = os.getenv("OO_TMP_DIR", "/tmp")


def get_db_url(platform: Platform) -> str:
    """Get the database URL for the given platform."""

    base_dir = os.path.expanduser("~/.openoligo")
    if platform in (Platform.RPI, Platform.BB):
        base_dir = os.path.join(tmp_dir, "openoligo")
    db_url = f"sqlite://{os.path.join(base_dir, 'openoligo.db')}"

    return db_url


async def db_init(url: str):
    """Initialize the database."""

    await Tortoise.init(
        db_url=url, modules={"models": ["openoligo.api.models"]}
    )  # pragma: no cover
    await Tortoise.generate_schemas()  # pragma: no cover
