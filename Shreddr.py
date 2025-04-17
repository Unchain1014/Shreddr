import os
import tkinter as tk
import uuid
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def rename_file(file_path):
    """Renames the file to a random UUID to obscure metadata."""
    new_name = str(uuid.uuid4())
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    return new_path

def shred_file(file_path, passes=3):
    """Overwrites the file with random bytes multiple times, renames it, and deletes it."""
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"File {file_path} is empty. Skipping overwrite.")
        else:
            for _ in range(passes):
                with open(file_path, "wb") as f:
                    f.write(os.urandom(file_size))  # Overwrite with random bytes
                file_path = rename_file(file_path)  # Rename the file after each pass
        os.remove(file_path)  # Delete the file
        return True
    except Exception as e:
        print(f"Error shredding file {file_path}: {e}")
        return False

def on_file_drop(event):
    """Handles file drop events and initiates shredding."""
    file_path = event.data.strip()
    # Remove curly braces if present
    if file_path.startswith("{") and file_path.endswith("}"):
        file_path = file_path[1:-1]
    if os.path.isfile(file_path):
        success = shred_file(file_path)
        if success:
            # Show confirmation prompt
            messagebox.showinfo("Shreddr", f"File successfully shredded and deleted:\n{file_path}")
    else:
        print(f"Invalid file: {file_path}")

# Create a simple drag-and-drop GUI
root = TkinterDnD.Tk()
root.title("Shreddr")
root.geometry("250x250")
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_file_drop)

# Update label styling
label = tk.Label(root, text="DROP FILES HERE", font=("Arial", 10, "bold"), fg="#666666")
label.pack(expand=True, fill=tk.BOTH)

root.mainloop()