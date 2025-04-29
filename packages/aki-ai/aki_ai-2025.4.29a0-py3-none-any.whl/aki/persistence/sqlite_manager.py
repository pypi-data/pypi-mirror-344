"""
SQLite database manager implementation.
"""

import logging
import os
from pathlib import Path

from chainlit.data import BaseDataLayer

from aki.persistence.chainlit_sqlite_adapter import ChainlitSQLiteAdapter
from aki.persistence.database_manager import DatabaseManager
from aki.persistence.local_file_storage import LocalFileStorageClient


class SQLiteManager(DatabaseManager):
    """
    SQLite implementation of the DatabaseManager interface.
    """

    def _setup_database_url(self):
        """Initialize SQLite manager with connection details."""
        # Get the database path from environment or use default
        db_path = os.getenv(
            "AKI_SQLITE_PATH", str(Path.home() / ".aki" / "database.sqlite")
        )
        self.db_path = os.path.expanduser(db_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Create connection URL and set it to environment for other components
        self._async_database_url = f"sqlite+aiosqlite:///{self.db_path}"
        os.environ["AKI_SQLITE_URL"] = self._async_database_url

    @property
    def db_type(self) -> str:
        """Return the database type identifier."""
        return SQLiteManager.__name__

    def _get_sql_schema_filename(self):
        return "database_schema_sqlite.sql"

    async def init_db(self) -> None:
        await self._initialize_schema()

    def get_adapter(self) -> BaseDataLayer | None:
        """Return a ChainlitSQLiteAdapter for the database."""
        try:
            # Create a storage provider for elements
            storage_provider = LocalFileStorageClient()

            return ChainlitSQLiteAdapter(
                conninfo=self._async_database_url,
                show_logger=False,
                storage_provider=storage_provider,
            )
        except Exception as e:
            logging.error(f"Failed to create SQLite adapter: {e}", exc_info=True)
            return None
