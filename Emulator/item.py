from dataclasses import dataclass

MAIN = "main"
SUBLANE1 = "sublane1"
SUBLANE2 = "sublane2"
SUBLANE3 = "sublane3"

@dataclass
class Item: # Ein Item / Stückgut

    item_id: int
    creation_time: float 
    lane: str = MAIN
    distance: float = 0.0