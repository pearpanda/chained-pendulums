from typing import Union, List, Tuple
from pathlib import Path
import numpy as np


def load_pendulum_file(path: Union[str, Path]) -> np.ndarray:
    return np.loadtxt(path)


def load_states_file(path: Union[str, Path]) -> np.ndarray:
    return np.loadtxt(path)


def load_times_file(path: Union[str, Path]) -> np.ndarray:
    return np.loadtxt(path)
