import subprocess
import webbrowser
import socket
import time
import argparse

def wait_for_port(host: str, port: int, timeout: float = 10.0):
    """Wait until a TCP port is open."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                sock.connect((host, port))
                return True
            except (ConnectionRefusedError, socket.timeout):
                time.sleep(0.2)
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Fava launcher', description='Launch fava and open beancount file when ready.')
    parser.add_argument('-a', '--address', required=True, help='fava IP address')
    parser.add_argument('-p', '--port', type=int, required=True, help='fava port')
    parser.add_argument('-f', '--file', required=True, help='fava IP address')
    args = parser.parse_args()

    beancount_file = args.file
    host, port = args.address, args.port

    # Start Fava in the background
    proc = subprocess.Popen(
        ["fava", "--host", host, "--port", str(port), beancount_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(f"Starting Fava at http://{host}:{port} ...")

    # Wait until Fava is ready
    if wait_for_port(host, port, timeout=15):
        print("Fava is ready! Opening browser...")
        webbrowser.open(f"http://{host}:{port}/")
    else:
        print("Fava did not start within the timeout period.")

    # Keep script running until Fava exits
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
