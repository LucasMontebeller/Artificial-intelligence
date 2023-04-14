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
    
    def reflex_vacuum_iterate(self, iterations):
        result = cont = 0
        while cont < iterations:
            result += self.reflex_vacuum_agent()
            self.reset()
            cont+=1

        return result / iterations


# estados iniciais
def main():

    TIME_STEPS = int(1e3)

    # da para melhorar a lógica em um dicionário de estados
    cleaner_right_dirty = VacuumCleaner(TIME_STEPS, Locations.RIGHT, States.DIRTY)
    cleaner_right_clean = VacuumCleaner(TIME_STEPS, Locations.RIGHT, States.CLEAN)
    cleaner_left_dirty = VacuumCleaner(TIME_STEPS, Locations.LEFT, States.DIRTY)
    cleaner_left_clean = VacuumCleaner(TIME_STEPS, Locations.LEFT, States.CLEAN)

    results = [
        cleaner_right_dirty.reflex_vacuum_iterate(TIME_STEPS), 
        cleaner_right_clean.reflex_vacuum_iterate(TIME_STEPS),
        cleaner_left_dirty.reflex_vacuum_iterate(TIME_STEPS),
        cleaner_left_clean.reflex_vacuum_iterate(TIME_STEPS)
    ]

    print(f""" Resultados para {TIME_STEPS} iterações:
        cleaner_right_dirty => {results[0]} 
        cleaner_right_clean => {results[1]}
        cleaner_left_dirty => {results[2]}
        cleaner_left_clean => {results[3]}""")
    

if __name__ == "__main__":
    main()
    