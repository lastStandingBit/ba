from dataclasses import dataclass

@dataclass
class PlantParameter: # Feste Anlageparameter
    tick: float = 0.01 #10ms tick
    main_length: float = 2.0 # main fördebrand länge : 2m
    sub_length: float = 1.0 # sub
    diverter_position: float = 1.8 # div position "auf förderband"
    item_creation_period: float = 1.0 # 1 sekunde abstand zum objekt davor, erstellt quelle ein objekt

Default_PlantParameter = PlantParameter()

min_speed = 0.0
max_speed = 2.0

@dataclass
class RuntimeParameter: # einstellbare Laufzeitparameter von Dt einstellbar
    run: bool = False  # run förderband
    main_speed: float = 0.5 # m/s
    routing_mode: str = "ROUND_ROBIN"
    target_lane: int = 1
    
Default_RuntimeParameter = RuntimeParameter()


server_endpoint = "opc.tcp://0.0.0.0:4840/Testumgebung"
server_namespace_uri = "urn:fh:DT-Testumgebung:Förderbandsystem-Emulation"







