# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cliffxrd (Clifford Hattingh)
# AURA: Agentic Unified Recollection Archive

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import closing

logger = logging.getLogger(__name__)


class AndroidStudioScraper:
    """Extracts chat messages and context from Android Studio local SQLite databases."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def scrape(self) -> List[Dict[str, Any]]:
        """Connects to SQLite database and extracts chat history."""
        conversations = []
        if not self.db_path.exists():
            logger.error(f"Android Studio database not found at {self.db_path}")
            return conversations

        try:
            with closing(
                sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            ) as conn:
                conn.row_factory = sqlite3.Row
                with closing(conn.cursor()) as cursor:
                    # Attempt to extract messages, schema depends on actual studio version
                    # This uses a typical fallback schema for IDE chat histories
                    cursor.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name='messages';"
                    )
                    if not cursor.fetchone():
                        logger.warning("No 'messages' table found in DB.")
                        return conversations

                    cursor.execute("""
                        SELECT id, session_id, role, content, timestamp 
                        FROM messages 
                        ORDER BY session_id, timestamp ASC
                    """)

                    rows = cursor.fetchall()
                    sessions: Dict[str, List[Dict[str, Any]]] = {}

                    for row in rows:
                        session_id = str(row["session_id"])
                        msg = {
                            "id": row["id"],
                            "role": row["role"],
                            "content": row["content"],
                            "timestamp": row["timestamp"],
                        }
                        if session_id not in sessions:
                            sessions[session_id] = []
                        sessions[session_id].append(msg)

                    for sess_id, msgs in sessions.items():
                        conversations.append(
                            {
                                "source": "Android Studio",
                                "session_id": sess_id,
                                "message_count": len(msgs),
                                "messages": msgs,
                                "status": "Scraped Successfully",
                            }
                        )

        except sqlite3.Error as e:
            logger.error(f"SQLite error reading {self.db_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {e}")

        return conversations
