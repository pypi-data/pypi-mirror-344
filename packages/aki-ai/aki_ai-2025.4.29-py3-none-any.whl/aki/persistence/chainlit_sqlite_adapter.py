import json
from typing import Dict, List, Optional

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.data.storage_clients.base import BaseStorageClient
from chainlit.element import ElementDict
from chainlit.logger import logger
from chainlit.types import (
    ThreadDict,
)


class ChainlitSQLiteAdapter(SQLAlchemyDataLayer):
    """
    Custom adapter for Chainlit to work with SQLite databases.
    This class overrides the methods that use PostgreSQL-specific ON CONFLICT syntax
    with SQLite-compatible INSERT OR REPLACE syntax.
    """

    def __init__(
        self,
        conninfo: str,
        ssl_require: bool = False,
        storage_provider: BaseStorageClient | None = None,
        user_thread_limit: int | None = 1000,
        show_logger: bool | None = False,
    ):
        super().__init__(
            conninfo=conninfo,
            ssl_require=ssl_require,
            storage_provider=storage_provider,
            user_thread_limit=user_thread_limit,
            show_logger=show_logger,
        )

    async def update_thread(
        self,
        thread_id: str,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ):
        if self.show_logger:
            logger.info(f"SQLAlchemy: update_thread, thread_id={thread_id}")

        user_identifier = None
        if user_id:
            user_identifier = await self._get_user_identifer_by_id(user_id)

        data = {
            "id": thread_id,
            "createdAt": (
                await self.get_current_timestamp() if metadata is None else None
            ),
            "name": (
                name
                if name is not None
                else (metadata.get("name") if metadata and "name" in metadata else None)
            ),
            "userId": user_id,
            "userIdentifier": user_identifier,
            "tags": json.dumps(tags) if tags else None,
            "metadata": json.dumps(metadata) if metadata else None,
        }
        parameters = {
            key: value for key, value in data.items() if value is not None
        }  # Remove keys with None values
        columns = ", ".join(f'"{key}"' for key in parameters.keys())
        values = ", ".join(f":{key}" for key in parameters.keys())
        updates = ", ".join(
            f'"{key}" = EXCLUDED."{key}"' for key in parameters.keys() if key != "id"
        )
        query = f"""
            INSERT INTO threads ({columns})
            VALUES ({values})
            ON CONFLICT ("id") DO UPDATE
            SET {updates};
        """
        await self.execute_sql(query=query, parameters=parameters)

    async def get_all_user_threads(
        self, user_id: Optional[str] = None, thread_id: Optional[str] = None
    ) -> Optional[List[ThreadDict]]:
        threads = await super().get_all_user_threads(user_id, thread_id)
        return (
            None
            if threads is None
            else [
                {
                    **thread,
                    "tags": json.loads(thread["tags"]),
                    "metadata": json.loads(
                        thread["metadata"]
                    ),  # Convert metadata back to dict
                }
                for thread in threads
            ]
        )

    async def get_element(
        self, thread_id: str, element_id: str
    ) -> Optional["ElementDict"]:
        """Get an element by ID."""
        try:
            query = """
                SELECT id, name, type, url, display, language, size, chainlitKey as "chainlitKey", forId as "forId",
                    props, threadId as "threadId", objectKey as "objectKey", mime
                FROM elements
                WHERE id = :element_id AND threadId = :thread_id;
            """
            result = await self.execute_sql(
                query, {"element_id": element_id, "thread_id": thread_id}
            )

            if not result or not isinstance(result, list) or len(result) == 0:
                return None
                
            # Get the first row from the result list
            row = result[0]
            element = ElementDict(**{**row, "id": str(row["id"])})

            if element.get("objectKey") and self.storage_provider:
                # Get the URL for the file
                element["url"] = self.storage_provider.get_read_url(
                    element["objectKey"]
                )

            return element

        except Exception as e:
            logger.error(f"Error getting element: {e}")
            return None

    async def create_element(self, element):
        """Create a new element."""
        try:
            if not self.storage_provider:
                logger.warning("Storage provider not configured. Element not created.")
                return

            # Handle file uploads if needed
            if hasattr(element, "path") and element.path and self.storage_provider:
                object_key = self.storage_provider.upload_file(element.path)
                element.objectKey = object_key

            # Prepare data for insertion
            data = {
                "id": element.id,
                "name": element.name,
                "threadId": element.thread_id,
                "forId": getattr(element, "forId", None),
                "type": getattr(element, "type", None),
                "display": getattr(element, "display", None),
                "language": getattr(element, "language", None),
                "size": getattr(element, "size", None),
                "chainlitKey": getattr(element, "chainlitKey", None),
                "props": json.dumps(getattr(element, "props", {})),
                "objectKey": getattr(element, "objectKey", None),
                "mime": getattr(element, "mime", None),
                "url": getattr(element, "url", None),
            }

            # Filter out None values
            data = {k: v for k, v in data.items() if v is not None}

            # Build the query
            columns = ", ".join(f'"{key}"' for key in data.keys())
            values = ", ".join(f":{key}" for key in data.keys())

            query = f"""
                INSERT INTO elements ({columns})
                VALUES ({values})
            """

            await self.execute_sql(query=query, parameters=data)
            logger.info(f"Created element: {element.id}, {element.name}")

        except Exception as e:
            logger.error(f"Error creating element: {e}")

    async def delete_element(self, element_id: str, thread_id: Optional[str] = None):
        """Delete an element by ID."""
        try:
            # First get the element to get the object key
            if thread_id:
                element = await self.get_element(thread_id, element_id)

                if element and element.get("objectKey") and self.storage_provider:
                    # Delete the file from storage
                    self.storage_provider.delete_file(element["objectKey"])

            # Build the WHERE clause
            where_clause = "id = :element_id"
            params = {"element_id": element_id}

            if thread_id:
                where_clause += " AND threadId = :thread_id"
                params["thread_id"] = thread_id

            query = f"""
                DELETE FROM elements
                WHERE {where_clause}
            """

            await self.execute_sql(query=query, parameters=params)
            logger.info(f"Deleted element: {element_id}")

        except Exception as e:
            logger.error(f"Error deleting element: {e}")
