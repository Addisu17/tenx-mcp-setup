# Minimal File-Based Notes App

This is a minimal GUI-first, file-based note-taking app implemented in Python.

Run the app:

```bash
python notes_app.py
```

Notes are saved as Markdown files under the `notes_data/` folder created next to the project root.

Files added:

- `notes/storage.py` — simple storage backend (list/read/save/delete/search)
- `notes_app.py` — Tkinter GUI launcher (list, new, open, edit, delete, save)

This is a bare-minimum starting point. Next steps: add tagging, richer metadata, tests, and a CLI bridge.
