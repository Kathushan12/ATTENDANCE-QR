from sqlalchemy import engine_from_config, pool
from alembic import context
import os

from app.db.base import Base
from app.db import models  # noqa: F401

config = context.config

DATABASE_URL = os.environ.get("DATABASE_URL")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
