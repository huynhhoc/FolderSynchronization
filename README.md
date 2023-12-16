# Folder Synchronization Program

## Overview

This program is designed to synchronize two folders: a source folder and a replica folder. The synchronization is one-way, ensuring that the content of the replica folder is modified to exactly match the content of the source folder. The synchronization process is performed periodically, and file creation/copying/removal operations are logged to both a file and the console output.

## Algorithm Explanation for async_synchronize_folders Function

The ``async_synchronize_folders`` function is responsible for synchronizing the contents of two folders: the ``source folder`` and the ``replica folder``. This process is performed asynchronously to improve efficiency, utilizing the asyncio library in Python. The algorithm follows these key steps:

    * Create Directories in Replica:
        - Iterate through the directories in the source folder using os.walk.
        - For each directory found, construct the corresponding directory path in the replica folder.
        - If the directory does not exist in the replica, create it.
        - Log the creation of directories to provide feedback.

    * Collect Existing Files and Directories in Replica:
        - Traverse the ``replica folder`` using os.walk.
        - Maintain sets to store the existing directories (``existing_dirs_in_replica``) and files (``existing_files_in_replica``) in the ``replica``.
        - Populate these sets to keep track of the current state of the ``replica``.

    * Iterate Through Source Files and Directories:
        - Again, traverse the ``source folder`` using os.walk.
        - For each source directory, construct the corresponding path in the replica.
        - Remove the directory path from ``existing_dirs_in_replica`` to mark it as encountered.
        - For each source file, construct the corresponding path in the ``replica``.
        - Check if the file exists in the ``replica``.

    * Copy New Files to Replica:
        - If a file in the source does not exist in the replica, log the action and initiate an asynchronous copy using ``async_copy_file``.
        - This step ensures that new files in the source are copied to the replica.

    * Update Modified Files in Replica:
        - If a file exists in both the ``source`` and the ``replica``, compare their modification timestamps and sizes.
        - If the source file is newer or has a different size, log the action and initiate an asynchronous copy to update the file in the replica.
        - Update the source state dictionary to reflect the new state.

    * Remove Stale Files and Directories from Replica:
        - Iterate through the remaining files and directories in ``existing_files_in_replica`` and ``existing_dirs_in_replica``.
        - Log the removal of each file or directory.
        - Delete the corresponding file or directory from the replica.

    * Asynchronous File Copy:
        - The ``async_copy_file`` function is utilized to perform asynchronous file copy operations.
        - It reads the content from the ``source file`` and writes it to the ``destination file`` in separate threads, making the process more efficient.

    * Synchronize All Operations:
        Use await asyncio.gather(*tasks) to synchronize all asynchronous copy operations initiated during the process.

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