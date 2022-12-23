#!/usr/bin/env python
import asyncio
from mavsdk import System
from termcolor import colored
from mavsdk.offboard import (OffboardError, PositionNedYaw)

class Base:
    def __init__(self,number):
        self.number = number
        self.absolute_altitude=0
        port = int("1403"+str(self.number))
        self.drone = System(port=port)
        self.base_latitude_deg = 47.3977419
        self.base_longitude_deg = 8.5455936
    async def connect(self):
        print(colored("-- Connecting drone{}".format(self.number),'yellow'))
        await self.drone.connect(system_address="udp://:1403{}".format(str(self.number)))

        print(colored("-- Testing connect for drone{}".format(self.number),'yellow'))
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print(colored("-- Connected to drone{}!".format(self.number),'green'))
                break

    async def takeoff(self):
        print(colored("-- Drone {} Taking off".format(self.number),'yellow'))
        try:     
            await self.drone.action.arm()
            await asyncio.sleep(2)
            await self.drone.action.takeoff()
            print(colored("-- Drone {} Taked off".format(self.number),'green'))
        except Exception as e:
            print(colored("-- Error:When drone {} taking off".format(self.number),'red')) 
            print(colored(e,'red'))
        
    async def goto_gps(self,pos):
        
        await self.drone.action.goto_location(pos[0],pos[1],pos[2]+self.absolute_altitude, 0)
        print(colored("-- Drone{} going to ({},{},{})".format(self.number,pos[0],pos[1],pos[2]),'green'))


    async def get_location2gps(self):
        async for position in self.drone.telemetry.position():
            latitude_deg = position.latitude_deg
            longitude_deg = position.longitude_deg
            relative_altitude_m = position.relative_altitude_m
            break
        return {'latitude_deg':latitude_deg,
        'longitude_deg':longitude_deg,
        'relative_altitude_m':relative_altitude_m}

    async def get_location2base(self):
        async for position in self.drone.telemetry.position():
            x = (position.latitude_deg-self.base_latitude_deg)*111000
            y =(position.longitude_deg-self.base_longitude_deg)*111000
            relative_altitude_m = position.relative_altitude_m
            break
        return {'x':x,
        'y':y,
        'relative_altitude_m':relative_altitude_m}


    async def get_degree(self):
        async for degree in self.drone.telemetry.attitude_euler():
            roll = degree.roll_deg
            pitch = degree.pitch_deg
            yaw = degree.yaw_deg
            break
        return {'roll':roll,'pitch':pitch,'yaw':yaw}
    
    async def get_homeposition(self):
        async for position in self.drone.telemetry.home():
            home_latitude_deg = position.latitude_deg
            home_longitude_deg = position.longitude_deg
            home_relative_altitude_m = position.relative_altitude_m
            break
        return {'home_latitude_deg':home_latitude_deg,
        'home_longitude_deg':home_longitude_deg,
        'home_relative_altitude_m':home_relative_altitude_m}

    async def goto_ned(self,pos):
        print(colored("-- Setting initial setpoint",'yellow'))
        await self.drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

        print(colored("-- Starting offboard",'green'))
        try:
            await self.drone.offboard.start()
        except OffboardError as error:
            print(colored(f"Starting offboard mode failed with error code: {error._result.result}",'red'))
            print("-- Disarming")
            await self.drone.action.disarm()
            return
        await self.drone.offboard.set_position_ned(PositionNedYaw(pos[0],pos[1],pos[2],pos[3]))

class Drone:
    def __init__(self,number):
        self.base = Base(number)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.base.connect())  

    def takeoff(self): 
        self.loop.run_until_complete(self.base.takeoff())

    def get_degree(self):
        return self.loop.run_until_complete(self.base.get_degree())

    def get_location2gps(self):
        return self.loop.run_until_complete(self.base.get_location2gps())

    def get_location2base(self):
        return self.loop.run_until_complete(self.base.get_location2base())

    def get_homeposition(self):
        return self.loop.run_until_complete(self.base.get_homeposition())

    def goto_gps(self,pos):
        self.loop.run_until_complete(self.base.goto_gps(pos))

    def goto_ned(self,pos):
        self.loop.run_until_complete(self.base.goto_ned(pos))