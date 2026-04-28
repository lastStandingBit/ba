from dataclasses import dataclass


@dataclass
class PlantParameter: # Feste Anlageparameter
    tick: float = 0.01 #10ms tick
    main_length: float = 2.0 # main fördebrand länge : 2m
    sub_length: float = 1.0 # sub
    diverter_position: float = 1.8 # div position "auf förderband"
    item_creation_period: float = 1.0 # 1 sekunde abstand zum objekt davor, erstellt quelle ein objekt

Default_PlantParameter = PlantParameter()












