"""
Conviniences for initializing the database.
"""
from tortoise import Tortoise

from openoligo.hal.platform import Platform


def get_db_url(platform: Platform) -> str:
    """Get the database URL for the given platform."""
    # if not platform:
    #    logging.error("Platform not supported.")
    #    raise RuntimeError("No platform detected")

    db_url = "sqlite://openoligo.db"
    if platform in (Platform.RPI, Platform.BB):
        db_url = "sqlite:////var/log/openoligo.db"

    return db_url


async def db_init(url: str):
    """Initialize the database."""

    await Tortoise.init(
        db_url=url, modules={"models": ["openoligo.api.models"]}
    )  # pragma: no cover
    await Tortoise.generate_schemas()  # pragma: no cover
