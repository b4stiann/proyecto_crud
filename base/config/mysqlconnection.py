import os
from typing import Any, Dict, List, Optional
import pymysql.cursors


class MySQLConnection:
    """Lightweight MySQL connection helper using PyMySQL.

    This mirrors the familiar Coding Dojo-style helper with a small twist:
    connection parameters are read from environment variables when present.
    """

    def __init__(self, db: str) -> None:
        self.db = db
        self.connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=db,
            port=int(os.getenv("MYSQL_PORT", "3306")),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query: str, data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            # Attempt to fetch; if no rows are returned (INSERT/UPDATE/DELETE), return the lastrowid
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return list(result)
            return [{"lastrowid": cursor.lastrowid}]


def connectToMySQL(db: str) -> MySQLConnection:
    return MySQLConnection(db)

