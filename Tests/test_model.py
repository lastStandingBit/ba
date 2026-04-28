from Emulator.plant_parameter import *
from Emulator.runtime_parameter import *
from Emulator.conveyor_model import *
from Emulator.item import *



# assert = testet ob etwas wahr oder falsch ist

### modelltest

# model wird korrekt erzeugt + reset erzeugt Anfangszustand

def test_create_model():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    assert model.plant.tick == 0.01
    assert model.plant.main_length == 2.0
    assert model.plant.sub_length == 1.0
    assert model.plant.diverter_position == 1.8
    assert model.plant.item_creation_period == 1.0


    assert model.active_Runtime.run == False
    assert model.active_Runtime.lane_speed == 0.5 
    assert model.active_Runtime.routing_mode == "ROUND_ROBIN"
    assert model.active_Runtime.target_lane == SUBLANE1

    assert model.state == STATE_STOPPED
    assert model.tick_counter == 0
    assert model.simulation_time == 0.0
    assert model.items_list == []
    assert model.kpis.throughput_all == 0
    assert model.next_item_id == 1
    assert model.item_creation_period == 0.0
    assert model.rr_rotation == 0
    assert model.last_event == "reset"


### command run test

# command run startet korrekt
def test_command_run_with_true():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    model.command_run(True)

    assert model.state == STATE_RUNNING
    assert model.last_event == "run_ON"
    assert model.active_Runtime.run == True

# command run bleibt gestoppt
def test_command_run_with_false():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    model.command_run(False)

    assert model.state == STATE_STOPPED
    assert model.last_event == "run_OFF"
    assert model.active_Runtime.run == False

# command run stoppt nach start
def test_command_run_false_after_true():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    model.command_run(True)
    model.command_run(False)

    assert model.state == STATE_STOPPED
    assert model.last_event == "run_OFF"
    assert model.active_Runtime.run == False

    ### create item test 

def test_create_item():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    model.create_item()
    model.create_item()
    item1 = model.items_list[0]
    item2 = model.items_list[1]

    assert item1.item_id == 1
    assert item2.item_id == 2
    assert model.last_event == "Item-Nr : 2"

### create item loop 

def test_item_loop_creation():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    
    model.tick_counter = 0
    model.create_item_loop()

    assert len(model.items_list) == 0

def test_item_loop_creation_false():

    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    
    model.tick_counter = model.ticks_per_item
    model.create_item_loop()

    assert len(model.items_list) == 1
    assert model.items_list[0].item_id == 1

### test for wip

def test_update_wip():
     
     model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    
     model.create_item()
     model.create_item()
     model.update_kpis()
     

     assert model.kpis.wip == 2

def test_kpi_state_wip():
     
     model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

     model.create_item()
     model.create_item()
     model.update_kpis()

     assert model.current_kpi_state() == {
          "throughput_all" : 0,
            "throughput_sublane1" : 0,
            "throughput_sublane2" : 0,
            "throughput_sublane3" : 0,
            "wip" : 2
     }


### test for selecting correct lane 

def test_select_lane_target_lane():

        model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

        model.active_Runtime.routing_mode == ROUTING_TARGET

        assert model.active_Runtime.target_lane == SUBLANE1

def test_select_lane_rr():
     
        model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

        model.active_Runtime.routing_mode = ROUTING_ROUND_ROBIN

        assert model.select_lane() == SUBLANE1
        assert model.select_lane() == SUBLANE2
        assert model.select_lane() == SUBLANE3
        assert model.select_lane() == SUBLANE1
        assert model.select_lane() == SUBLANE2
        assert model.select_lane() == SUBLANE3
        assert model.select_lane() == SUBLANE1

### test for correct itemmmovement

def test_for_item_on_main():
     
    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)

    model.create_item()
    item = model.items_list[0]
    model.item_on_main()

    assert item.lane == MAIN
    assert item.distance > 0 

def test_for_item_on_main_correct_after_diverter():
     
    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    model.active_Runtime.routing_mode = ROUTING_ROUND_ROBIN
    model.create_item()
    item = model.items_list[0]
    item.distance = model.plant.diverter_position #1.8
    model.item_on_main()

    assert model.rr_rotation == 1
    assert item.lane == SUBLANE1

def test_for_item_on_main_correct_after_diverter_lane2():
     
    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    model.active_Runtime.routing_mode = ROUTING_ROUND_ROBIN
    model.rr_rotation = 1
    model.create_item()
    item = model.items_list[0]
    item.distance = model.plant.diverter_position #1.8
    model.item_on_main()

    assert model.rr_rotation == 2
    assert item.lane == SUBLANE2

def test_for_item_on_main_correct_after_diverter_lane3():
     
    model = ConveyorModel(Default_PlantParameter,Default_RuntimeParameter)
    model.active_Runtime.routing_mode = ROUTING_ROUND_ROBIN
    model.rr_rotation = 2
    model.create_item()
    item = model.items_list[0]
    item.distance = model.plant.diverter_position #1.8
    model.item_on_main()

    assert model.rr_rotation == 3
    assert item.lane == SUBLANE3

### test for simulationstep



    



