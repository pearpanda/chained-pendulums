from pydantic import BaseModel
from typing import List


class Times(BaseModel):
    times: List[float]

