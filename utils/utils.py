# Author: Huynh Thai Hoc
import argparse
from typing import Any
import logging
import sys
import os
#-------------------------------------------------------------------------------------------------------------------------------------------
def get_args() -> Any:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    arg = parser.add_argument
    arg(
        "-s",
        "--source_path",
        default='./source',
        type=str,
        help="Path to the source folder",
        required=False,
    )
    arg(
        "-rep",
        "--replica_path",
        default= './replica',
        type=str,
        help="Path to the replica folder",
        required=False,
    )
    arg(
        "-in",
        "--sync_interval",
        default= 30,
        type=int,
        help="Synchronization interval in seconds",
        required=False,
    )
    arg(
        "-log",
        "--log_file",
        default= './logs/log.csv',
        type=str,
        help="Path to the log file",
        required=False,
    )

    return parser.parse_args()

#-----------------------------------------------------------------------------------
def logfile(log_file):
    """
    Set up logging configuration and return a logger.

    Returns:
        logging.Logger: Configured logger.
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s','%m-%d-%Y %H:%M:%S')

    # Create the directory if it doesn't exist
    directory = os.getcwd() + os.path.dirname(log_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(stdout_handler)
    return log