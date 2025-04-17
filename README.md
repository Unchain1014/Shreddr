# Shreddr

A lightweight, portable drag-and-drop tool for securely shredding and deleting files. Shreddr overwrites file data with random bytes, renames the file to obscure metadata, and then permanently deletes it.

## How It Works

1. **File Overwriting**:
   - Shreddr overwrites the file's contents multiple times with random bytes, making the original data difficult to recover.

2. **File Renaming**:
   - Between overwrite passes, Shreddr renames the file to a random UUID to obscure its metadata (e.g., file name, timestamps).

3. **File Deletion**:
   - After overwriting and renaming, the program permanently deletes the file.

4. **Drag-and-Drop Interface**:
   - The program provides a simple GUI where users can drag and drop files to shred them.

5. **Confirmation Prompt**:
   - After successfully shredding a file, Shreddr displays a confirmation dialog to notify the user.

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
- **Confirmation Prompt**: Notifies the user upon successful shredding.

## Limitations

- **SSD Wear Leveling**:
   - On SSDs, wear leveling may prevent complete overwriting of data. For SSDs, consider using tools that support TRIM commands or secure erase.
- **Physical Destruction**:
   - For the highest level of security, physical destruction of the storage medium is recommended.

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

1. Launch the program by running Shreddr.py.
2. Drag and drop files into the program window to shred them.
2. After shredding, a confirmation dialog will appear to notify you of the successful operation.

## Disclaimer

Shreddr is designed for casual use and may not meet the requirements for advanced data recovery prevention. Use at your own risk, and ensure you have backups of important files before shredding them, as this process is irreversible.