"""
utils/data_handler.py
Handles secure saving of candidate session data (local JSON, GDPR-lite).
"""

import json
import os
import hashlib
from datetime import datetime


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


class DataHandler:
    """Persists candidate screening sessions to local JSON files."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

    def save_candidate(self, candidate: dict, messages: list) -> str:
        """
        Anonymise PII, save session to data/ directory.
        Returns the session file path.
        """
        # Anonymise sensitive fields for storage
        safe = self._anonymise(candidate.copy())

        session = {
            "session_id":   self._session_id(candidate),
            "timestamp":    datetime.utcnow().isoformat() + "Z",
            "candidate":    safe,
            "message_count": len(messages),
            "tech_answers": candidate.get("tech_answers", {}),
        }

        filename = f"session_{session['session_id']}.json"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session, f, indent=2, ensure_ascii=False)

        return filepath

    # ── Private helpers ──────────────────────────────────────────────────────

    def _anonymise(self, candidate: dict) -> dict:
        """Hash email & phone; keep other fields as-is for recruiter review."""
        if "email" in candidate and candidate["email"]:
            candidate["email"] = self._hash(candidate["email"])
        if "phone" in candidate and candidate["phone"]:
            candidate["phone"] = self._hash(candidate["phone"])
        return candidate

    def _hash(self, value: str) -> str:
        return "hash:" + hashlib.sha256(value.encode()).hexdigest()[:12]

    def _session_id(self, candidate: dict) -> str:
        seed = candidate.get("email", "") + candidate.get("full_name", "") + datetime.utcnow().isoformat()
        return hashlib.md5(seed.encode()).hexdigest()[:10]
