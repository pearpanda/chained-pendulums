from typing import List
from pydantic import BaseModel


class PendulumState(BaseModel):
    angle: float = 0.0
    angular_velocity: float = 0.0


class PendulumStateChain(BaseModel):
    states: List[PendulumState]
