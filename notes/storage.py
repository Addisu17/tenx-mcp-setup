from pathlib import Path
from typing import List, Optional
import re
import uuid

# Notes are stored as plain Markdown files under a workspace-level `notes_data/` folder.
NOTES_DIR: Path = Path(__file__).parent.parent / "notes_data"


def _ensure_dir() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_filename(title: str) -> str:
    if not title:
        return str(uuid.uuid4())
    # keep letters, digits, dash, underscore; replace others with _
    name = title.strip()
    name = re.sub(r"[^\w\- ]+", "", name)
    name = name.replace(" ", "_")
    if not name:
        return str(uuid.uuid4())
    return name


def list_notes() -> List[str]:
    """Return list of note names (filename stems) sorted by name."""
    _ensure_dir()
    notes = []
    for p in NOTES_DIR.glob("*.md"):
        if p.is_file():
            notes.append(p.stem)
    return sorted(notes)


def read_note(name: str) -> Optional[str]:
    """Return the text content of the note named `name` or None if missing."""
    _ensure_dir()
    p = NOTES_DIR / f"{name}.md"
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def save_note(title: str, content: str) -> str:
    """Save `content` under a sanitized filename derived from `title`.

    Returns the note name (filename stem) used.
    """
    _ensure_dir()
    name = _sanitize_filename(title)
    p = NOTES_DIR / f"{name}.md"
    p.write_text(content or "", encoding="utf-8")
    return name


def delete_note(name: str) -> bool:
    """Delete note file. Returns True if deleted, False if not found."""
    _ensure_dir()
    p = NOTES_DIR / f"{name}.md"
    if p.exists():
        p.unlink()
        return True
    return False


def search_notes(query: str) -> List[str]:
    """Naive full-text search: return note names containing `query` (case-insensitive)."""
    _ensure_dir()
    q = query.lower()
    matches = []
    for name in list_notes():
        text = read_note(name) or ""
        if q in text.lower() or q in name.lower():
            matches.append(name)
    return matches
