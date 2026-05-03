"""Action parsing and normalization utilities."""

import re
from typing import List, Optional

VALID_ACTIONS = {"up", "down", "left", "right"}


def normalize_action(token: str) -> Optional[str]:
    """Normalize a single token to a valid action, or return None."""
    token = token.strip().lower()
    if token in VALID_ACTIONS:
        return token
    return None


def extract_actions(text: str) -> Optional[List[str]]:
    """
    Extract a valid action sequence from free-form model output.

    Strategy:
    1. Try to find tokens that are valid actions, ignoring punctuation/extra tokens.
    2. Return None if no valid actions found.
    """
    if not text or not text.strip():
        return None

    # Split on whitespace and common separators (comma, semicolon, pipe, slash)
    raw_tokens = re.split(r"[\s,;|/]+", text.strip())
    actions = []
    for tok in raw_tokens:
        # Strip leading/trailing punctuation
        tok = tok.strip(".,!?;:\"'()[]{}")
        normalized = normalize_action(tok)
        if normalized is not None:
            actions.append(normalized)

    if not actions:
        return None
    return actions


def actions_to_str(actions: List[str]) -> str:
    """Convert a list of actions to a space-separated string."""
    return " ".join(actions)


def str_to_actions(s: str) -> Optional[List[str]]:
    """Parse a space-separated action string. Returns None if any token is invalid."""
    if not s or not s.strip():
        return None
    tokens = s.strip().split()
    result = []
    for tok in tokens:
        if tok not in VALID_ACTIONS:
            return None
        result.append(tok)
    return result if result else None
