from pydantic import BaseModel
from typing import List


class Pendulum(BaseModel):
    mass: float
    length: float


class PendulumChain(BaseModel):
    pendulums: List[Pendulum]
