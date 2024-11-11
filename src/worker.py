import threading
import time
import os
from .logger import logs

def read_file_periodically(source_file_path, copy_file_path, interval):
    while True:
        if os.path.isfile(source_file_path) and os.access(source_file_path, os.R_OK):
            logs(f"Worker is reading {source_file_path}")
            with open(source_file_path, 'r') as source_file:
                source_content = source_file.read()

            if os.path.isfile(copy_file_path) and os.access(copy_file_path, os.R_OK):
                with open(copy_file_path, 'r') as copy_file:
                    copy_content = copy_file.read()

                if source_content != copy_content:
                    logs(f"Difference detected between {source_file_path} and {copy_file_path}")
                    handle_difference(source_content, copy_content, source_file_path, copy_file_path)
            else:
                logs(f"File {copy_file_path} does not exist. Creating it.")
                handle_difference(source_content, "", source_file_path, copy_file_path)
        else:
            logs(f"Cannot read file: {source_file_path}")
        time.sleep(interval)

def handle_difference(source_content, copy_content, source_file_path, copy_file_path):
    logs(f"Handling difference detected")
    source_lines = source_content.splitlines()
    copy_lines = copy_content.splitlines()

    with open(copy_file_path, 'w') as copy_file:
        for i, line in enumerate(source_lines):
            if i < len(copy_lines) and line != copy_lines[i]:
                logs(f"Updating line {i + 1} in {copy_file_path}")
            copy_file.write(line + '\n')

def start_worker(source_file_path, copy_file_path, interval):
    if not os.path.isfile(source_file_path):
        logs(f"Source file path {source_file_path} does not exist.")
        return
    if not os.access(source_file_path, os.R_OK):
        logs(f"Source file path {source_file_path} is not readable.")
        return

    worker = threading.Thread(target=read_file_periodically, args=(source_file_path, copy_file_path, interval))
    worker.daemon = True
    worker.start()
    logs(f"Worker has started for file: {source_file_path}")