# Author: Huynh Thai Hoc
from utils.utils import *
import os
import asyncio
import shutil
#--------------------------------------------------------------------------------
async def async_copy_file(src, dest):
    with open(src, 'rb') as src_file, open(dest, 'wb') as dest_file:
        content = await asyncio.to_thread(src_file.read)
        await asyncio.to_thread(dest_file.write, content)
#--------------------------------------------------------------------------------
async def async_synchronize_folders(source_path, replica_path, logging, source_state):
    # Create directories in replica if they don't exist
    for root, dirs, files in os.walk(source_path):
        for dir_name in dirs:
            dir_path_src = os.path.join(root, dir_name)
            dir_path_replica = dir_path_src.replace(source_path, replica_path)
            if not os.path.exists(dir_path_replica):
                logging.info(f"Creating directory: {dir_path_replica}")
                os.makedirs(dir_path_replica, exist_ok=True)

    tasks = []
    existing_files_in_replica = set()
    existing_dirs_in_replica = set()

    for root, dirs, files in os.walk(replica_path):
        for dir_name in dirs:
            dir_path_replica = os.path.join(root, dir_name)
            existing_dirs_in_replica.add(dir_path_replica)
        for file_name in files:
            file_path_replica = os.path.join(root, file_name)
            existing_files_in_replica.add(file_path_replica)

    for root, dirs, files in os.walk(source_path):
        for dir_name in dirs:
            dir_path_src = os.path.join(root, dir_name)
            dir_path_replica = dir_path_src.replace(source_path, replica_path)
            # Remove file from the set of existing files in the replica
            existing_dirs_in_replica.discard(dir_path_replica)
        
        for file_name in files:
            file_path_src = os.path.join(root, file_name)
            file_path_replica = file_path_src.replace(source_path, replica_path)

            # Check if the file exists in the replica
            if not os.path.exists(file_path_replica):
                logging.info(f"Copying new file: {file_path_replica}")
                tasks.append(async_copy_file(file_path_src, file_path_replica))
            else:
                # Check if the file needs to be updated
                replica_stat = (os.stat(file_path_replica).st_mtime, os.stat(file_path_replica).st_size)
                src_stat = (os.stat(file_path_src).st_mtime, os.stat(file_path_src).st_size)
                if source_state.get(file_path_src) != src_stat and replica_stat != src_stat:
                    logging.info(f"Updating file: {file_path_replica}")
                    tasks.append(async_copy_file(file_path_src, file_path_replica))
                    # Update source state after confirming the file exists in the replica
                    source_state[file_path_src] = src_stat

            # Remove file from the set of existing files in the replica
            existing_files_in_replica.discard(file_path_replica)

    # Remove files in replica that don't exist in the source
    for file_path_replica_to_remove in existing_files_in_replica:
        logging.info(f"Removing file: {file_path_replica_to_remove}")
        os.remove(file_path_replica_to_remove)

    # Remove directories in replica that don't exist in the source
    for dir_path_replica_to_remove in existing_dirs_in_replica:
        logging.info(f"Removing directory: {dir_path_replica_to_remove}")
        shutil.rmtree(dir_path_replica_to_remove)

    await asyncio.gather(*tasks)
#--------------------------------------------------------------------------------
def setup_logging(log_file_path, logging):
    logging.basicConfig(filename=log_file_path,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

async def main(args, logging):
    source_state = {}  # Dictionary to track source state
    while True:
        await async_synchronize_folders(args.source_path, args.replica_path, logging,source_state)
        logging.info('Synchronization completed successfully.')
        logging.info('Synchronization process sleep in around {} seconds.'.format(args.sync_interval))
        await asyncio.sleep(args.sync_interval)

if __name__ == "__main__":
    args= get_args()
    logging = logfile(args.log_file)
    asyncio.run(main(args, logging))