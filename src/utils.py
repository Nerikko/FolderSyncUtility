from .logger import logs
import os

def verifyPaths(source, replica, log_path):
    paths = [source, replica, os.path.dirname(log_path)]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
            logs(f"Path {path} created.")
        else:
            logs(f"Path {path} verified.")