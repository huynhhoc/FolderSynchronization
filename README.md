# Folder Synchronization Program

## Overview

This program is designed to synchronize two folders: a source folder and a replica folder. The synchronization is one-way, ensuring that the content of the replica folder is modified to exactly match the content of the source folder. The synchronization process is performed periodically, and file creation/copying/removal operations are logged to both a file and the console output.

## Author

    Huynh Thai Hoc

## Usage

To run the program, execute the main.py script with the following command-line arguments:

    --source_path: The path to the source folder.
    --replica_path: The path to the replica folder.
    --sync_interval: The interval (in seconds) at which synchronization should be performed periodically.
    --log_file: The path to the log file for recording synchronization operations.

## Example:

```

python main.py --source_path /path/to/source --replica_path /path/to/replica --sync_interval 3600 --log_file /path/to/sync_log.txt

```
## Dependencies

This program requires the following dependencies:

    Python 3.x
    asyncio (standard library)

## Implementation Details

The program is implemented in Python and utilizes asynchronous programming for efficient folder synchronization. The synchronization logic is implemented in the async_synchronize_folders function. File operations are logged to both the console and a specified log file.
Source Code Structure

    main.py: The main script to be executed for running the synchronization program.
    utils/utils.py: Utility functions, including argument parsing and logging setup.

## How to Run

    Install Python 3.x on your system if not already installed.
    Clone the repository or download the source code.
    Open a terminal or command prompt and navigate to the project directory.
    Run the program using the provided command-line arguments as described in the "Usage" section.

## Notes

    Ensure that the source folder and replica folder paths are correctly specified.
    The synchronization interval determines how frequently the program checks for updates in the source folder.
    Review the log file for detailed information on synchronization operations