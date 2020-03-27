from typing import List
from pydantic import BaseModel

from pendulum.model import Pendulum, PendulumState


class PendulumWithState(BaseModel):
    pendulum: Pendulum
    initial_state: PendulumState


class PendulumWithStateChain(BaseModel):
    pendulums: List[PendulumWithState]
