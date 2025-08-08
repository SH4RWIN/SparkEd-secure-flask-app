import os
import time
import socket
import subprocess

# Get DB connection info from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))

# Wait for the database to be available
def wait_for_db(host, port, timeout=60):
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"Database is up at {host}:{port}")
                return
        except OSError:
            if time.time() - start > timeout:
                raise TimeoutError(f"Timed out waiting for DB at {host}:{port}")
            print("Waiting for PostgreSQL...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db(DB_HOST, DB_PORT)
    print("Running setup.py to create tables if needed...")
    subprocess.run(["python", "setup.py"], check=True)
    print("Starting Gunicorn...")
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:5000", "app:app"])
