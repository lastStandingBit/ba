from dataclasses import dataclass
from .item import *

@dataclass
class RuntimeParameter: # einstellbare Laufzeitparameter von Dt einstellbar
    run: bool = False  # run förderband
    lane_speed: float = 0.5 # m/s
    routing_mode: str = "ROUND_ROBIN"
    target_lane: int = SUBLANE1
    
Default_RuntimeParameter = RuntimeParameter()

min_speed = 0.0
max_speed = 2.0