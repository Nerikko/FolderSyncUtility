import os
import threading
import time
from .logger import logs
from .worker import start_worker

# Dictionary to monitor active threads for each file
active_workers = {}

def count_files(source):
    readable_files = 0
    unreadable_files = 0
    path = source

    if os.path.isdir(path):
        for name in os.listdir(path):
            file_path = os.path.join(path, name)
            if os.path.isfile(file_path):
                if os.access(file_path, os.R_OK):
                    readable_files += 1
                else:
                    unreadable_files += 1
        logs(f"Number of readable files in {path}: {readable_files}")
        logs(f"Number of unreadable files in {path}: {unreadable_files}")

    elif os.path.isfile(path):
        if os.access(path, os.R_OK):
            readable_files = 1
            logs(f"Number of readable files in {path}: {readable_files}")
        else:
            unreadable_files = 1
            logs(f"Number of unreadable files in {path}: {unreadable_files}")

    else:
        logs(f"The path '{path}' is neither a valid file nor a directory.")
        raise ValueError(f"The path '{path}' is neither a valid file nor a directory.")

    if readable_files == 0:
        raise ValueError(f"No readable files found in the path '{path}'.")

    return readable_files, unreadable_files

def initializeWorkers(source, replica, interval):
    if os.path.isdir(source):
        for file_name in os.listdir(source):
            source_file_path = os.path.join(source, file_name)
            replica_file_path = os.path.join(replica, file_name)

            if source_file_path not in active_workers:
                # Start a worker for the file if it is not already active
                logs(f"Starting worker for {source_file_path}...")
                start_worker(source_file_path, replica_file_path, interval)
                active_workers[source_file_path] = True
                logs(f"Worker for {source_file_path} started.")
            else:
                logs(f"Worker for {source_file_path} is already running.")
    else:
        logs(f"The source path '{source}' is not a directory.")

def monitor_new_files(source, replica, interval):
    while True:
        initializeWorkers(source, replica, interval)
        time.sleep(interval)

def initialize(source, replica, interval):
    count_files(source)
    initializeWorkers(source, replica, interval)
    monitor_thread = threading.Thread(target=monitor_new_files, args=(source, replica, interval))
    monitor_thread.daemon = True
    monitor_thread.start()