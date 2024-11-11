import argparse
import signal
import sys
from src import globalInitialize
from src.logger import initialize_logger

SOURCE = None
REPLICA = None
LOG_PATH = None
INTERVAL = 30  # Default interval

def signal_handler(sig, frame):
    print('Terminating the program...')
    sys.exit(0)

def main():
    global SOURCE, REPLICA, LOG_PATH, INTERVAL

    parser = argparse.ArgumentParser(description="Folder synchronization program.")
    parser.add_argument("source", help="Path to the source folder.")
    parser.add_argument("replica", help="Path to the replica folder.")
    parser.add_argument("log_path", help="Path to the log file.")
    parser.add_argument("interval", nargs='?', type=int, default=30, help="Synchronization interval in seconds (default: 30).")

    args = parser.parse_args()

    SOURCE = args.source
    REPLICA = args.replica
    LOG_PATH = args.log_path
    INTERVAL = args.interval

    initialize_logger(LOG_PATH)
    globalInitialize(SOURCE, REPLICA, LOG_PATH, INTERVAL)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to terminate the program.')

    while True:
        signal.pause()

if __name__ == "__main__":
    main()