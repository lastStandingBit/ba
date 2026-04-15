from Emulator.parameter import *
from Emulator.conveyor_model import *

def test_model_initial_state():
    model = ConveyorModel(Default_ServerParameter,
                          Default_RuntimeParameter,
                          Default_SpeedLimits)
    snapshot = model.status_snapshot()

    assert snapshot["state"] == "STOPPED"
    assert snapshot["tick"] == 0
    