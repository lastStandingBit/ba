from dataclasses import dataclass

MAIN = 0
SUBLANE1 = 1
SUBLANE2 = 2
SUBLANE3 = 3

@dataclass
class Item: # Ein Item / Stückgut

    item_id: int
    creation_time: float 
    lane: int = MAIN
    distance: float = 0.0