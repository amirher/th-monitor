"""
Thornleigh Farm Monitor
Database Module
author: hugh@blinkybeach.com
"""
import psycopg2
from typing import Optional
from typing import Any


class Database:
    """
    A connection to a PostgreSQL database
    """
    def __init__(self, dsn: str, insertion_query: str) -> None:

        assert isinstance(dsn, str)
        self._dsn = dsn
        self._connection = psycopg2.connect(dsn=self._dsn)
        self._cursor = self._connection.cursor()

        self._insertion_query = insertion_query

        return

    def _connect(self) -> None:
        """
        Establish a connection to the PostgreSQL server
        """
        self._connection = psycopg2.connect(dsn=self._dsn)
        self._cursor = self._connection.cursor()
        return

    def execute(
        self,
        query: str,
        arguments: Optional[dict] = None
    ) -> Optional[Any]:

        try:
            self._cursor.execute(query, arguments)
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            try:
                self._connection.close()
                self._cursor.close()
            except Exception:
                pass
            self._connect()
            self._cursor.execute(query, arguments)
        if self._cursor.description is None:
            return None
        result = self._cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def insert(self, data: str) -> None:
        """
        Insert sample data into the database
        """
        self.execute(self._insertion_query, {'sample_data': data})
        return
