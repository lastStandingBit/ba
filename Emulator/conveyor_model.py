from dataclasses import dataclass
from typing import Literal
from .parameter import *
from .interface_settings import *


Lane = Literal[1,2,3] #notwendig?
Section = Literal["main","sub1","sub2","sub3"] #literal hat geholfen

state = STATE_STOPPED
tick = 0.0
simulation_time = 0.0
items_list = [] # leert itemliste

next_item_id = 0
item_creation_period = 0.0 # quelltimer neu
rr_rotation = 0 # rr bei 0
last_event = "reset"

@dataclass
class Item: # Ein Item / Stückgut

    item_id: int
    creation_time: float
    lane: Lane | None
    section: Section = "main"
    distance: float = 0.0

@dataclass
class KpiState:

    throughput_all: int = 0
    throughput_lane_1: int = 0
    throughput_lane_2: int = 0
    throughput_lane_3: int = 0
    wip: int = 0

kpis = KpiState() 

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
        
        self.ticks_per_item = int(plant.item_creation_period / plant.tick)

        self.reset() # damit konstr startzustand sauber initialisieren kann
        
        # ControlParameter = standard
        # active ControlParameter = aktuell aktive
        

        # noch reset def machen
        # snapshot def ?

    def command_run(self, bool:bool) -> None:
        # bool absichern vor komischen inputs # kann später bei tests fehlschlagen wegen falshchen input und nachhinein hier absichern + gut für zeigen von debugging
        self.active_Runtime.run = bool # setzt im aktuellen laufzeitobjekt den wert von bool (true oder false)
        if bool == True:
            self.state = STATE_RUNNING
            self.last_event = "run_ON"
        else:
            self.state = STATE_STOPPED
            self.last_event = "run_OFF"

    def reset(self) -> None:
            
        self.state = STATE_STOPPED
        self.tick_counter = 0.0
        self.simulation_time = 0.0
        self.items_list = [] # leert itemliste
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
    
    def create_item(self): # so ist das gut fürs testen, item ertsellung kann man quasi alleine testen ohne quelle und automatischer erzeugungsloop
       item = Item(item_id=self.next_item_id, creation_time=self.simulation_time, lane= None, section= "main", distance= 0.0)
       #nächstes item definieren, dann liste appenden
       self.next_item_id =+1
       self.items_list.append(item)
       self.last_event = f"item :{item.item_id}" 

    def create_item_loop(self) -> None:
        if self.tick_counter > 0 and self.tick_counter % self.ticks_per_item == 0: # erst nach 0 ticks beginnt, also nach 1 sekunde kommt erstes item
            self.create_item()

        

    def status_snapshot(self) -> dict[str, object]:
        return{
            "state" : self.state,
            "simulation_time": self.simulation_time,
            "tick": self.tick,
            "last_event": self.last_event
        }


        




    

