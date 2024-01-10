import os
from importlib import reload
from unittest.mock import patch

import openoligo.utils.sim as simulation_params
from openoligo.hal.types import Platform

# assuming the file is named `simulation_params.py`


def test_simulation_speedup_env_var_set():
    with patch.dict(os.environ, {"OO_SIM_SPEED": "500"}):
        reload(simulation_params)  # This will reload the module with new environment
        from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR

        assert (
            SIMULATION_SPEEDUP_FACTOR == 500
        ), "Simulation speedup factor should be 500, if environment variable is set to 500"


def test_simulation_speedup_env_var_not_set_sim_platform():
    with patch("openoligo.hal.types.__platform__", new=Platform.SIM):
        reload(simulation_params)
        from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR

        assert SIMULATION_SPEEDUP_FACTOR == 1000


def test_simulation_speedup_env_var_not_set_non_sim_platform():
    with patch("openoligo.hal.types.__platform__", new=Platform.BB):
        # Assuming there's a different platform
        reload(simulation_params)
        from openoligo.utils.sim import SIMULATION_SPEEDUP_FACTOR

        assert SIMULATION_SPEEDUP_FACTOR == 1
