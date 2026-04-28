from .opc_ua_server import *
import asyncio
from .plant_parameter import *
from .runtime_parameter import *

from .conveyor_model import *
from .interface_settings import*



async def async_main() -> None:
    model = ConveyorModel(Default_PlantParameter, Default_RuntimeParameter)

    server = OpcuaServer(model)
    await server.init()
    await server.serve()

def main() -> None:
    asyncio.run(async_main())

if __name__ == "__main__":
    main()