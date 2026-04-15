from dataclasses import dataclass
from typing import Literal
from .parameter import *
from .interface_settings import *


Lane = Literal[1,2,3] #notwendig?
Section = Literal["main","sub1","sub2","sub3"] #literal hat geholfen

@dataclass
class Item: # Ein Item / Stückgut

    item_id: int
    creation_time: float
    lane: Lane
    section: Section = "main"
    distance: float = 0.0

@dataclass
class KpiState:

    throughput_all: int = 0
    throughput_lane_1: int = 0
    throughput_lane_2: int = 0
    throughput_lane_3: int = 0
    wip: int = 0

def current_kpi_snapshot(self) -> dict[str,int]:

    return {
        "throughput_all" : self.throughput_all,
        "throughput_lane_1" : self.throughput_lane_1,
        "throughput_lane_2" : self.throughput_lane_2,
        "throughput_lane_3" : self.throughput_lane_3,
        "wip" : self.wip
    }

class ConveyorModel:

    def __init__(self, plant : PlantParameter, runtime : RuntimeParameter) -> None:
        # Unser dauerhafte Plantparameter
        self.plant = plant 
        # Standard ControlParameter gespeichert
        self.runtime = RuntimeParameter(run = runtime.run,
                                        main_speed = runtime.main_speed,
                                        routing_mode = runtime.routing_mode,
                                        target_lane = runtime.target_lane) 
        # aktive Controlparameter
        self.active_Runtime = RuntimeParameter (run = runtime.run, 
                                                main_speed = runtime.main_speed,
                                                routing_mode = runtime.routing_mode, 
                                                target_lane = runtime.target_lane)
        self.reset() # damit konstr startzustand sauber initialisieren kann
        
        # ControlParameter = standard
        # active ControlParameter = aktuell aktive
        

        # noch reset def machen
        # snapshot def ?

    def reset(self) -> None:
            
        self.state = STATE_STOPPED
        self.tick = 0.0
        self.simulation_time = 0.0
        self.items = [] # leert itemliste
        self.kpis = KpiState() # alle kpis auf standard
        self.next_item_id = 0
        self.item_creation_period = 0.0 # quelltimer neu
        self.rr_rotation = 0 # rr bei 0
        self.last_event = "reset"


        # aktuelle bedienung wieder auf standard gesetzt
        self.active_Runtime = RuntimeParameter(
            run = self.runtime.run,
            main_speed = self.runtime.main_speed,
            routing_mode = self.runtime.routing_mode,
            target_lane = self.runtime.target_lane
        )

        

    def status_snapshot(self) -> dict[str, object]:
        return{
            "state" : self.state,
            "simulation_time": self.simulation_time,
            "tick": self.tick,
            "last_event": self.last_event
        }


        




    

