# Folder Synchronization Tool

This Python script synchronizes two folders: a source folder and a replica folder. It maintains a full, identical copy of the source folder in the replica folder, performing a one-way synchronization. The synchronization happens periodically, and all file operations (creation, copying, removal) are logged to both a file and the console.

There are two versions of this tool:
* Using shutil.copytree(): A version that leverages the built-in shutil.copytree() for copying entire directories. sync_folders.py
* Manual Synchronization: A version that avoids shutil.copytree() in case that was not allowed for the task. sync_folders_v2.py



## Features

* **One-way Synchronization:** Changes in the source folder are reflected in the replica folder. Content in the replica folder that does not exist in the source is removed.
* **Periodic Synchronization:** The script runs continuously, synchronizing the folders at a user-defined interval.
* **Logging:** All file operations (copying, creating, removing) are logged with timestamps and log levels to both the console and a specified log file.
* **Command-Line Arguments:** The paths to the source and replica folders, the synchronization interval, and the log file path are configured using command-line arguments.
* **Standard Library Usage:** The script primarily relies on built-in Python modules, avoiding external libraries for core folder synchronization logic.

## Prerequisites

* Python 3.x installed on your system.

## Usage

1.  **Save the script:** Save the provided Python code.

2.  **Run from the command line:** Open your terminal or command prompt and navigate to the directory where you saved the script. Execute the script with the required arguments:

    ```bash
    python sync_folders_v2.py <source_folder_path> <replica_folder_path> [-i <interval_seconds>] [-l <log_file_path>]
    ```

    **Arguments:**

    * `<source_folder_path>`: The path to the source folder you want to copy. **(Required, positional)**
    * `<replica_folder_path>`: The path to the replica folder where the synchronized copy will be maintained. **(Required, positional)**
    * `-i <interval_seconds>`, `--interval <interval_seconds>`: The time interval (in seconds) between synchronization attempts. Defaults to `600` seconds (10 minutes). **(Optional)**
    * `-l <log_file_path>`, `--log_path <log_file_path>`: The path to the log file where synchronization activities will be recorded. Defaults to `sync_log.txt` in the current directory. **(Optional)**

    **Example:**

    To synchronize the folder `/home/user/source_data` to `/home/user/replica_backup` every 30 minutes and log to `backup.log`:

    ```bash
    python sync_folders_v2.py /home/user/source_data /home/user/replica_backup -i 1800 -l backup.log
    ```

3.  **Running the script:** Once executed, the script will start the initial synchronization and then periodically synchronize the folders based on the specified interval. You will see log messages in your console, and the same information will be written to the log file.

4.  **Stopping the script:** To stop the synchronization process, press `Ctrl+C` in your terminal. The script will log a message indicating that it was stopped by the user.
