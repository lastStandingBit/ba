from .plant_parameter import *
from .runtime_parameter import *
from .kpi_state import *
from .item import *
from .interface_settings import *

class ConveyorModel:

    def __init__(self, plant : PlantParameter, runtime : RuntimeParameter) -> None:
        # Unser dauerhafte Plantparameter
        self.plant = plant 
        # Standard ControlParameter gespeichert
        self.runtime = RuntimeParameter(run = runtime.run,
                                        lane_speed = runtime.lane_speed,
                                        routing_mode = runtime.routing_mode,
                                        target_lane = runtime.target_lane) 
        # aktive Controlparameter
        self.active_Runtime = RuntimeParameter (run = runtime.run, 
                                                lane_speed = runtime.lane_speed,
                                                routing_mode = runtime.routing_mode, 
                                                target_lane = runtime.target_lane)
        
        self.ticks_per_item = int(self.plant.item_creation_period / self.plant.tick)

        self.state = STATE_STOPPED
        self.tick_counter = 0
        self.simulation_time = 0.0
        self.items_list = [] # leert itemliste
        self.items_list_to_remove = []
        self.kpis = KpiState() # alle kpis auf standard
        self.next_item_id = 1
        self.item_creation_period = 0.0 # quelltimer neu
        self.rr_rotation = 0 # rr bei 0
        self.last_event = "reset"

        self.reset() # damit konstr startzustand sauber initialisieren kann
        
        # ControlParameter = standard
        # active ControlParameter = aktuell aktive
        

        # noch reset def machen
        # snapshot def ?
    def reset(self) -> None:
            
        self.state = STATE_STOPPED
        self.tick_counter = 0.0
        self.simulation_time = 0.0
        self.items_list = [] # leert itemliste
        self.kpis = KpiState() # alle kpis auf standard
        self.next_item_id = 1
        self.item_creation_period = 0.0 # quelltimer neu
        self.rr_rotation = 0 # rr bei 0
        self.last_event = "reset"
        # aktuelle bedienung wieder auf standard gesetzt
        self.active_Runtime.run = self.runtime.run
        self.active_Runtime.lane_speed = self.runtime.lane_speed
        self.active_Runtime.routing_mode = self.runtime.routing_mode
        self.active_Runtime.target_lane = self.runtime.target_lane
    

    def command_run(self, bool:bool) -> None:
        # bool absichern vor komischen inputs # kann später bei tests fehlschlagen wegen falshchen input und nachhinein hier absichern + gut für zeigen von debugging
        self.active_Runtime.run = bool # setzt im aktuellen laufzeitobjekt den wert von bool (true oder false)
        if bool == True:
            self.state = STATE_RUNNING
            self.last_event = "run_ON"
        else:
            self.state = STATE_STOPPED
            self.last_event = "run_OFF"

    def current_kpi_state(self) -> dict[str,int]:
        return {
            "throughput_all" : self.kpis.throughput_all,
            "throughput_sublane1" : self.kpis.throughput_lane_1,
            "throughput_sublane2" : self.kpis.throughput_lane_2,
            "throughput_sublane3" : self.kpis.throughput_lane_3,
            "wip" : self.kpis.wip
        }

    
    def create_item(self): # so ist das gut fürs testen, item ertsellung kann man quasi alleine testen ohne quelle und automatischer erzeugungsloop
       item = Item(item_id=self.next_item_id, creation_time=self.simulation_time, lane= MAIN, distance= 0.0)
       #nächstes item definieren, dann liste appenden
       self.next_item_id += 1
       self.items_list.append(item)
       self.last_event = f"Item-Nr : {item.item_id}" 

    def create_item_loop(self) -> None:
        if self.tick_counter > 0 and self.tick_counter % self.ticks_per_item == 0: # erst nach 0 ticks beginnt, also nach 1 sekunde kommt erstes item
            self.create_item()
            
    def update_kpis(self) -> None:
        self.kpis.wip = len(self.items_list)

    def item_on_main(self) -> None:
        for item in self.items_list:
            item.distance += self.active_Runtime.lane_speed * self.plant.tick # Pos. Fortschrittsformel : x_2 = x_1 + v * delta t
            # Problem gefunden : wie auf item distance zugreifen wenn item nicht erzeugt
            # problem : wann muss diese methode denn aufgerufen werden?
            if item.distance >= self.plant.diverter_position:
                item.lane = self.select_lane()
                # gute enscheidung: nach weiche wird distance auf 0.0, bei fehler weiss man obs um die weiche geht, hätte distance auch mitnehmen
                item.distance = 0.0
                item.section = f"sublane{item.lane}"

                self.last_event = f"item {item.item_id} on {item.lane}"

            
            
                                    #formel
    
    def simulation_step(self) -> None: # simulationsschritt, zeitdiskret in  kleinen simulationsscrhritten
        if self.state == STATE_RUNNING:
            self.tick_counter +=1 # muss mitgezählt werden pro tick, auch um modulo zu erfüllen
            self.simulation_time += self.plant.tick # 0 + 0.01 = 0.01 nach 1 tick , 0.01 + 0.01 = 0.02 simulation time nach 2 Ticks / Simulationsschritten
            #man hätte simulations_time auch mit : tick_counter * tick berechen können
            self.create_item_loop() # ruft item erzeugung auf, agiert also quasi als quelle und wird durch simulations_step aufgerufen und quelle zum zeitlichen modellablauf gehört
            # hier direkt aufs main band?
            self.item_on_main()
            self.item_on_sublane()
        else:
            return # wenn modell nicht läuft, nichts machen, wieso sollten simulationsschritte weiter laufen? logisch


    def current_status_state(self) -> dict[str, object]:
        return{
            "state" : self.state,
            "simulation_time": self.simulation_time,
            "tick_counter": self.tick_counter,
            "last_event": self.last_event
        }
    
    def select_lane(self) -> int:
        if self.active_Runtime.routing_mode == ROUTING_TARGET:
            return self.active_Runtime.target_lane
        
        else:
            lane = (self.rr_rotation % 3)+1 # 1-lane1, 2-lane2,3-lane3  
            self.rr_rotation +=1
            return lane
    
    def item_on_sublane(self) -> None:

        for item in self.items_list:
            if item.lane == MAIN:
                continue
            item.distance += self.active_Runtime.lane_speed * self.plant.tick

            if item.distance >= self.plant.sub_length:
                self.kpis.throughput_all += 1

                if item.lane == SUBLANE1:
                    self.kpis.throughput_lane_1 +=1
                elif item.lane == SUBLANE2:
                    self.kpis.throughput_lane_2 +=1
                elif item.lane == SUBLANE3:
                    self.kpis.throughput_lane_3 +=1

                self.items_list_to_remove.append(item)
                self.last_event = f"item{item.item_id} out of lane {item.lane}"
        
        for item in self.items_list_to_remove:
            self.items_list.remove(item)


    



        




    

