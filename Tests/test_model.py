from Emulator.parameter import *
from Emulator.conveyor_model import *
from Emulator.item import *

# assert = testet ob etwas wahr oder falsch ist

### modelltest

# model wird korrekt erzeugt + reset erzeugt Anfangszustand


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

