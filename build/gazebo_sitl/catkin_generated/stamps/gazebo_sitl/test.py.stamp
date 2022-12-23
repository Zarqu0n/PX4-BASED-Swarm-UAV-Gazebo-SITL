import asyncio
from mavsdk import System



absolute_altitude = 10
async def run():
    drone = System(port=14030)
    await drone.connect(system_address="udp://:14030")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(3)
    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(3)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(47.397606, 8.543060, flying_alt, 0)

    while True:
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())