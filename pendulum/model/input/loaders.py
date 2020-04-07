from typing import Union, List, Tuple
from pathlib import Path
import numpy as np

from pendulum.model import Pendulum, PendulumState
from pendulum.model.pendulum_schema import PendulumChain
from pendulum.model.state_schema import PendulumStateChain
import pendulum.model.input.pendulum_state_schema as pws


def load_pendulum_file(path: Union[str, Path]) -> List[Pendulum]:
    pc = PendulumChain.parse_file(path)
    return pc.pendulums


def load_states_file(path: Union[str, Path]) -> List[PendulumState]:
    sc = PendulumStateChain.parse_file(path)
    return sc.states


def load_frame_split(pendulum_path: Union[str, Path],
                     states_path: Union[str, Path]) -> Tuple[List[Pendulum], List[PendulumState]]:
    """
    Loads the files containing the descriptions of the pendulums and their initial conditions (position and speed)

    By default, JSON is expected. It may work with other file formats (if pydantic supports them).
    Throws pydantic's ValidationError if the validation fails
    :param pendulum_path: Path to the file containing information about the pendulums
    :param states_path: Path to the file containing the pendulums' initial states
    :return: List of Pendulum objects describing individual pendulums
    """
    pc = load_pendulum_file(pendulum_path)
    sc = load_states_file(states_path)
    if len(pc) != len(sc):
        raise ValueError('All pendulums must have their initial conditions set')
    return pc, sc


def load_frame(path: Union[str, Path]) -> Tuple[List[Pendulum], List[PendulumState]]:
    psc = pws.PendulumWithStateChain.parse_file(path)
    pendulums = []
    states = []
    for ps in psc.pendulums:
        pendulums.append(ps.pendulum)
        states.append(ps.initial_state)
    return pendulums, states


def load_times_file(path: Union[str, Path]) -> np.ndarray:
    return np.loadtxt(path)
