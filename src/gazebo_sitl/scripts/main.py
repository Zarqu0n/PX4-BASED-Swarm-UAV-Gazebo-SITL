#!/usr/bin/env python
from drone import Drone
import asyncio
from termcolor import colored

class Main:

    def __init__(self):
        self.drone1 = Drone(0)

    def main(self):

        while 1:
            pos1 = [100, 0,-5,0]
            pos2 = [0, 100,-5,0]
            arg = input(colored('Command:','blue'))
            try:

                if arg == 'takeoff':
                    self.drone1.takeoff()

                elif arg == 'goto':

                    self.drone1.goto_ned(pos1)

                elif arg == 'pos':
                    print(self.drone1.get_location2base())


                    
            except Exception as e:
                print(colored(e,'red'))
                continue

if __name__ == "__main__":
    main = Main()
    main.main()