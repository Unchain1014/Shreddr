import os
import sys
import tkinter as tk
import uuid
import time
import winsound
from tkinter import messagebox, Toplevel, Label
from tkinterdnd2 import TkinterDnD, DND_FILES

# Flag to track if shredding is in progress
is_shredding = False

def rename_file(file_path):
    """Renames the file to a random UUID to obscure metadata."""
    new_name = str(uuid.uuid4())
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    return new_path

def shred_file(file_path, passes=3, progress_window=None):
    """Overwrites the file with random bytes multiple times, renames it, and deletes it."""
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            if progress_window:
                progress_window.update_status(f"File {file_path} is empty. Skipping overwrite.")
            print(f"File {file_path} is empty. Skipping overwrite.")
        else:
            for i in range(passes):
                if progress_window:
                    progress_window.update_status(f"Pass {i + 1}/{passes}: Overwriting file...")
                with open(file_path, "wb") as f:
                    f.write(os.urandom(file_size))  # Overwrite with random bytes
                time.sleep(0.1)  # Add a delay of 0.5 seconds
                if progress_window:
                    progress_window.update_status(f"Pass {i + 1}/{passes}: Renaming file...")
                file_path = rename_file(file_path)  # Rename the file after each pass
                time.sleep(0.1)  # Add a delay of 0.5 seconds
        if progress_window:
            progress_window.update_status("Deleting file...")
        time.sleep(0.1)  # Add a delay before deletion
        os.remove(file_path)  # Delete the file
        return True
    except Exception as e:
        if progress_window:
            progress_window.update_status(f"Error: {e}")
        print(f"Error shredding file {file_path}: {e}")
        return False

class ProgressWindow:
    """A simple popup window to show progress."""
    def __init__(self, root, title="Progress"):
        self.window = Toplevel(root)
        self.window.title(title)
        self.window.iconbitmap(icon_path)  # Set the icon for the progress window


        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set window dimensions
        window_width = 250
        window_height = 250

        # Calculate position to center the window and adjust 300px higher
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.label = Label(self.window, text="Starting...", font=("Arial", 10))
        self.label.pack(expand=True, fill=tk.BOTH)
        self.window.update()

    def update_status(self, message):
        """Update the status message in the popup."""
        self.label.config(text=message)
        self.window.update()

    def close(self):
        """Close the popup window."""
        self.window.destroy()

def on_file_drop(event):
    """Handles file drop events and initiates shredding for multiple files."""
    global is_shredding
    if is_shredding:
        messagebox.showwarning("Shreddr", "A shredding operation is already in progress. Please wait.")
        return

    # Debugging: Print raw event data
    print(f"Raw event data: {event.data}")

    # Split the dropped files into a list by curly braces and remove empty entries
    file_paths = [file_path.strip() for file_path in event.data.split("{") if file_path.strip()]
    file_paths = [file_path.strip("}") for file_path in file_paths]  # Remove trailing curly braces

    # Debugging: Print cleaned file paths
    print(f"Cleaned file paths: {file_paths}")

    # Filter out invalid file paths
    valid_files = [file_path for file_path in file_paths if os.path.isfile(file_path)]
    if not valid_files:
        messagebox.showerror("Shreddr", "No valid files were dropped.")
        return

    # Show confirmation prompt
    if not show_confirmation(valid_files):
        return  # Exit if the user selects "No"

    is_shredding = True  # Set the flag to indicate shredding is in progress
    successfully_deleted = []  # List to store successfully shredded files
    failed_to_delete = []  # List to store files that failed to shred

    for file_path in valid_files:
        # Create a progress window for each file
        progress_window = ProgressWindow(root, title=f"Shredding...")
        success = shred_file(file_path, progress_window=progress_window)
        progress_window.close()
        if success:
            successfully_deleted.append(os.path.basename(file_path))
        else:
            failed_to_delete.append(os.path.basename(file_path))

    is_shredding = False  # Reset the flag after all shredding is complete

    # Show a single summary prompt at the end
    show_summary(successfully_deleted, failed_to_delete)

def show_confirmation(valid_files):
    """Displays a scrollable confirmation prompt for the files to be shredded."""
    confirmation_window = Toplevel(root)
    confirmation_window.title("Confirm Shredding")
    confirmation_window.iconbitmap(icon_path)  # Set the icon for the confirmation window

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window dimensions
    window_width = 500
    window_height = 300

    # Calculate position to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    confirmation_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a frame for the text and scrollbar
    frame = tk.Frame(confirmation_window)
    frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=(25, 0))

    # Add a Text widget for the file list
    text_widget = tk.Text(frame, wrap=tk.WORD, height=10, font=("Arial", 10))
    text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Add the file list content
    confirmation_message = "The following files will be shredded:\n\n"
    confirmation_message += "\n".join([os.path.basename(file) for file in valid_files])
    text_widget.insert(tk.END, confirmation_message)
    text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

    # Add Yes and No buttons
    button_frame = tk.Frame(confirmation_window)
    button_frame.pack(pady=25)

    def confirm():
        # Construct the path to the audio file
        audio_path = os.path.abspath(os.path.join(base_path, "../audio/shred.wav"))
        print(f"Looking for audio file at: {audio_path}")  # Debugging: Print the resolved path
        
        # Check if the audio file exists
        if not os.path.isfile(audio_path):
            print(f"Error: Audio file not found at {audio_path}")
        else:
            try:
                # Attempt to play the audio file asynchronously
                winsound.PlaySound(audio_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                print(f"Error playing audio file: {e}")
        
        # Proceed with confirmation logic
        confirmation_window.destroy()
        root.confirmation_result = True

    def cancel():
        confirmation_window.destroy()
        root.confirmation_result = False

    yes_button = tk.Button(button_frame, text="Yes", command=confirm, width=10, height=1)
    yes_button.pack(side=tk.LEFT, padx=5)

    no_button = tk.Button(button_frame, text="No", command=cancel, width=10, height=1)
    no_button.pack(side=tk.LEFT, padx=5)

    # Set default result to False
    root.confirmation_result = False
    confirmation_window.wait_window()  # Wait for the user to close the window
    return root.confirmation_result

def show_summary(successfully_deleted, failed_to_delete):
    """Displays a scrollable summary of the shredding process."""
    summary_window = Toplevel(root)
    summary_window.title("Shreddr Summary")
    summary_window.iconbitmap(icon_path)  # Set the icon for the summary window

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window dimensions
    window_width = 500
    window_height = 300

    # Calculate position to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    summary_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a frame for the text and scrollbar
    frame = tk.Frame(summary_window)
    frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=(25, 0))  # Match padding to confirmation prompt

    # Add a Text widget for the summary
    text_widget = tk.Text(frame, wrap=tk.WORD, height=10, font=("Arial", 10))
    text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Add the summary content
    summary_message = "The following files were successfully shredded:\n\n"
    summary_message += "\n".join(successfully_deleted)
    if failed_to_delete:
        summary_message += "\n\nThe following files could not be shredded:\n\n"
        summary_message += "\n".join(failed_to_delete)

    text_widget.insert(tk.END, summary_message)
    text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

    # Add a close button
    button_frame = tk.Frame(summary_window)
    button_frame.pack(pady=25)  # Match button padding to confirmation prompt

    close_button = tk.Button(button_frame, text="Close", command=summary_window.destroy, width=10, height=1)
    close_button.pack(side=tk.LEFT, padx=5)

# Create a simple drag-and-drop GUI
root = TkinterDnD.Tk()
root.title("Shreddr")

# Set the application icon
if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
    base_path = sys._MEIPASS  # Path to the temporary folder created by PyInstaller
else:
    base_path = os.path.dirname(__file__)  # Path to the script directory

icon_path = os.path.join(base_path, "icon.ico")
root.iconbitmap(icon_path)  # Replace with the path to your .ico file

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window dimensions
window_width = 250
window_height = 250

# Calculate position to center the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_file_drop)

# Create a frame to hold the labels
label_frame = tk.Frame(root)
label_frame.pack(expand=True)

# Add the larger text above
title_label = tk.Label(
    label_frame,
    text="SHREDDR",
    font=("Arial", 20, "bold"),  # Slightly larger font
    fg="#CCCCCC"
)
title_label.pack()

# Add the "DROP FILES HERE" label
drop_label = tk.Label(
    label_frame,
    text="DROP FILES HERE",
    font=("Arial", 12, "bold"),
    fg="#CCCCCC"
)
drop_label.pack()

root.mainloop()