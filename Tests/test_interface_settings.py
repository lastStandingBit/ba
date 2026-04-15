
from Emulator.interface_settings import *

def test_interface_names_correct():
    assert COMMAND_RUN == "RUN"
    assert RESPONSE_STATE == "STATE"
    assert KPI_THROUGHPUT_1 == "THROUGHPUT_LANE_1"
