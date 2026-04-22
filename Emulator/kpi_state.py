from dataclasses import dataclass


@dataclass
class KpiState:

    throughput_all: int = 0
    throughput_lane_1: int = 0
    throughput_lane_2: int = 0
    throughput_lane_3: int = 0
    wip: int = 0