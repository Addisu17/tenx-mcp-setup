"""Minimal GUI-first file-based notes app (Tkinter).

Run `python notes_app.py` to launch a simple notes editor.
Notes are stored as Markdown files under `notes_data/` in the workspace.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
from notes.storage import list_notes, read_note, save_note, delete_note, search_notes


class NotesApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Notes - Minimal")
        root.geometry("900x600")

        self.left_frame = tk.Frame(root, width=250)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=6, pady=6)
        self.search_entry.bind("<Return>", lambda e: self.refresh_list())

        self.listbox = tk.Listbox(self.left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.open_selected())

        btn_frame = tk.Frame(self.left_frame)
        btn_frame.pack(fill=tk.X, padx=6, pady=6)
        tk.Button(btn_frame, text="New", command=self.new_note).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Delete", command=self.delete_note).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.RIGHT)

        self.editor = ScrolledText(root)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        bottom = tk.Frame(root)
        bottom.pack(fill=tk.X)
        tk.Button(bottom, text="Save", command=self.save_current).pack(side=tk.RIGHT, padx=6, pady=6)

        self.current_note = None
        self.refresh_list()

    def refresh_list(self):
        q = self.search_var.get().strip()
        if q:
            notes = search_notes(q)
        else:
            notes = list_notes()
        self.listbox.delete(0, tk.END)
        for n in notes:
            self.listbox.insert(tk.END, n)

    def open_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        name = self.listbox.get(sel[0])
        text = read_note(name) or ""
        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, text)
        self.current_note = name

    def new_note(self):
        title = simpledialog.askstring("New note", "Enter note title:")
        if title is None:
            return
        name = save_note(title, "")
        self.refresh_list()
        # select new note
        try:
            idx = list(self.listbox.get(0, tk.END)).index(name)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)
            self.open_selected()
        except ValueError:
            pass

    def save_current(self):
        content = self.editor.get("1.0", tk.END).rstrip("\n")
        if self.current_note:
            # reuse current name
            save_note(self.current_note, content)
            messagebox.showinfo("Saved", f"Saved {self.current_note}")
        else:
            # ask for title
            title = simpledialog.askstring("Save note", "Enter note title:")
            if not title:
                return
            name = save_note(title, content)
            self.current_note = name
            self.refresh_list()

    def delete_note(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Delete", "No note selected")
            return
        name = self.listbox.get(sel[0])
        if messagebox.askyesno("Delete", f"Delete note {name}? This cannot be undone."):
            delete_note(name)
            self.current_note = None
            self.editor.delete("1.0", tk.END)
            self.refresh_list()


def main():
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
