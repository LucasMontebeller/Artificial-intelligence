from enum import Enum
import random as rd

class Locations(Enum):
    LEFT = 1
    RIGHT = 2

class States(Enum):
    CLEAN = 0
    DIRTY = 1


class VacuumCleaner:

    def __init__(self, time_steps, initial_location, initial_state):
        self.time_steps = time_steps
        self.location = initial_location
        self.state = initial_state

    def reflex_vacuum_agent(self):
        cont = 0
        awards = 0
        while (cont < self.time_steps):
            if self.state == States.DIRTY:
                self.state = States.CLEAN
                awards+=1
            elif self.location == Locations.LEFT:
                self.location = Locations.RIGHT
            elif self.location == Locations.RIGHT:
                self.location = Locations.LEFT

            self.state = States(rd.randint(0, 1))
            cont+=1

        return awards

cleaner = VacuumCleaner(1000, Locations.RIGHT, States.DIRTY)
agent = cleaner.reflex_vacuum_agent()
print(agent)