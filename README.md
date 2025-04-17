# Shreddr

A lightweight, portable drag-and-drop tool for securely shredding and deleting files. Shreddr overwrites file data with random bytes, renames the file to obscure metadata, and then permanently deletes it.

![screenshot.png](/images/screenshot.PNG)

## How It Works

1. **File Overwriting**:
   - Shreddr overwrites the file's contents multiple times with random bytes, making the original data difficult to recover.

2. **File Renaming**:
   - Between overwrite passes, Shreddr renames the file to a random UUID to obscure its metadata (e.g., file name, timestamps).

3. **File Deletion**:
   - After overwriting and renaming, the program permanently deletes the file.

4. **Drag-and-Drop Interface**:
   - The program provides a simple GUI where users can drag and drop one or multiple files to shred them.

5. **Confirmation Prompt**:
   - Before shredding, Shreddr displays a Yes/No confirmation prompt listing all the files to be shredded. This prevents accidental shredding and allows users to review the files.

6. **Summary Prompt**:
   - After shredding, Shreddr displays a summary of all successfully shredded files and any files that failed to shred.

## Why Use Shreddr Instead of the Recycle Bin?

| **Aspect**            | **Recycle Bin**                                                                 | **Shreddr**                                                                                     |
|------------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **File Deletion**      | Files are only moved to the recycle bin and can be easily restored.             | Files are overwritten with random bytes, renamed, and permanently deleted.                     |
| **Data Recovery**      | Files can be recovered using basic tools, even after emptying the recycle bin. | Overwriting and renaming make recovery much harder, especially after multiple passes.           |
| **Metadata Removal**   | Metadata (e.g., file name, timestamps) remains intact.                         | Metadata is obscured by renaming the file to a random UUID during the shredding process.         |
| **Security**           | Minimal security; files are still present on the disk.                        | Provides a secure method of deletion, especially for casual use cases.                          |
| **Ease of Use**        | Simple drag-and-drop to the recycle bin.                                       | Shreddr also provides a drag-and-drop interface for ease of use.                                |

## Features

- **Secure File Shredding**: Overwrites file contents multiple times with random bytes.
- **Metadata Obfuscation**: Renames the file to a random UUID between overwrite passes.
- **Permanent Deletion**: Deletes the file after overwriting and renaming.
- **Drag-and-Drop GUI**: Built with `tkinterdnd2` for an intuitive user experience.
- **Multiple File Support**: Drag and drop multiple files at once to shred them in a single operation.
- **Confirmation Prompt**: Displays a Yes/No confirmation dialog listing all files to be shredded, preventing accidental shredding.
- **Summary Prompt**: Provides a summary of successfully shredded files and any failures.

## Limitations

- **SSD Wear Leveling**:
   - On SSDs, wear leveling may prevent complete overwriting of data. For SSDs, consider using tools that support TRIM commands or secure erase.
- **Advanced Forensic Recovery**:
   - While Shreddr is effective for most use cases, highly advanced forensic tools might still recover traces of the file. For highly sensitive data, consider physical destruction of the storage medium.

## Installation

1. Install Python (3.7 or later).
2. Install the required library for drag-and-drop functionality:
    ```bash
    pip install tkinterdnd2
3. Clone or download this repository.
4. Run the program:
    ```bash
    python Shreddr.py

## Usage

1. Launch the program by running `Shreddr.py`.
2. Drag and drop one or multiple files into the program window to shred them.
3. Review the list of files in the confirmation prompt and click "Yes" to proceed or "No" to cancel.
4. After shredding, a summary dialog will appear listing all successfully shredded files and any failures.

## Disclaimer

Shreddr is designed for casual use and may not meet the requirements for advanced data recovery prevention. Use at your own risk, and ensure you have backups of important files before shredding them, as this process is irreversible.