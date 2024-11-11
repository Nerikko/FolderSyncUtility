import threading
import queue
import os

log_queue = queue.Queue()
LOG_PATH = None

def writeLog(log):
    global LOG_PATH
    if LOG_PATH:
        with open(LOG_PATH, 'a') as file:
            file.write(log + '\n')
    else:
        print("LOG_PATH is not set. Cannot write log.")

def logs(log):
    log_queue.put(log)

def log_worker():
    while True:
        log = log_queue.get()
        if log is None:
            break
        writeLog(log)
        log_queue.task_done()

def initialize_logger(log_path):
    global LOG_PATH
    if not log_path:
        raise ValueError("LOG_PATH cannot be empty.")
    LOG_PATH = log_path
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        thread = threading.Thread(target=log_worker, daemon=True)
        thread.start()
        print(f"Log worker thread started successfully with thread ID: {thread.ident}")
    except RuntimeError as e:
        print(f"Failed to start log worker thread: {e}")
