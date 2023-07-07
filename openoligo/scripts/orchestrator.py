"""
A minimal script for running the server and the runner in parallel,
and keeping them alive for the whole time.
"""
import os
import subprocess
import sys

loop_forever = os.getenv("OO_LOOP_FOREVER", "true").lower() == "true"


def main() -> None:
    """
    Starts two subprocesses: Runner and Server and keeps them available for the whole time.
    """
    try:
        with subprocess.Popen(["oligo-server"], shell=True) as process:
            with subprocess.Popen(["oligo-runner"], shell=True) as runner:
                process.wait()
                runner.wait()
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
