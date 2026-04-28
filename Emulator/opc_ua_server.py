from conveyor_model import*


server_endpoint = "opc.tcp://0.0.0.0:4840/Testumgebung"
server_namespace_uri = "urn:fh:DT-Testumgebung:Förderbandsystem-Emulation"

class OpcuaServer:

    def __init__(self, model : ConveyorModel):
        pass