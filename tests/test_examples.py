import os
import subprocess
from unittest.mock import patch

import pytest


def test_examples():
    examples_dir = "examples"
    examples = [f for f in os.listdir(examples_dir) if f.endswith(".py")]
    print(examples)

    with patch.dict(os.environ, {"OO_SIM_SPEED": "10000"}):
        for example in examples:
            example_path = os.path.join(examples_dir, example)
            try:
                print("Running example: {}".format(example_path))
                subprocess.check_call(["python3", example_path])
                print(f"{example} ran successfully.")
            except subprocess.CalledProcessError as e:
                print(f"{example} failed with error code {e.returncode}.")
                pytest.fail(f"{example} failed with error code {e.returncode}.")
            except Exception as e:
                print(f"{example} failed with an exception: {e}")
                pytest.fail(f"{example} failed with an exception: {e}")
