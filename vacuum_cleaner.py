from enum import Enum, auto
import random as rd

class Locations(Enum):
    LEFT = auto()
    RIGHT = auto()

class States(Enum):
    CLEAN = auto()
    DIRTY = auto()

class VacuumCleaner:

    def __init__(self, time_steps, initial_location, initial_state):
        self.time_steps = time_steps
        self.location = initial_location
        self.state = initial_state
        self.score = 0

    def reset(self):
        self.score = 0


    def reflex_vacuum_agent(self):
        cont = 0
        while cont < self.time_steps:
            if self.state == States.DIRTY:
                self.state = States.CLEAN
                self.score+=1
            elif self.location == Locations.LEFT:
                self.location = Locations.RIGHT
            elif self.location == Locations.RIGHT:
                self.location = Locations.LEFT

            self.state = States(rd.randint(1, 2))
            cont+=1 

        return self.score / self.time_steps

# estados iniciais
cleaner_right_dirty = VacuumCleaner(1000, Locations.RIGHT, States.DIRTY)
cleaner_right_clean = VacuumCleaner(1000, Locations.RIGHT, States.CLEAN)
cleaner_left_dirty = VacuumCleaner(1000, Locations.LEFT, States.DIRTY)
cleaner_left_clean = VacuumCleaner(1000, Locations.LEFT, States.CLEAN)

cont = 0
results = [0, 0, 0, 0]
while cont < 1e6:
    results[0] += cleaner_right_dirty.reflex_vacuum_agent()
    results[1] += cleaner_right_clean.reflex_vacuum_agent()
    results[2] += cleaner_left_dirty.reflex_vacuum_agent()
    results[3] += cleaner_left_clean.reflex_vacuum_agent()

    cleaner_right_dirty.reset()
    cleaner_right_clean.reset()
    cleaner_left_dirty.reset()
    cleaner_left_clean.reset()
    cont+=1

print(f"""
        cleaner_right_dirty => {results[0]/1e6} 
        cleaner_right_clean => {results[1]/1e6}
        cleaner_left_dirty => {results[2]/1e6}
        cleaner_left_clean => {results[3]/1e6}""")