from enum import Enum, auto
import random as rd

class Locations(Enum):
    LEFT = auto()
    RIGHT = auto()

class States(Enum):
    CLEAN = auto()
    DIRTY = auto()

class AgentType(Enum):
    SIMPLE = auto()
    RANDOM = auto()
    MURPHY = auto()

class VacuumCleaner:

    def __init__(self, time_steps, initial_location, initial_state, agent_type):
        self.time_steps = time_steps
        self.location = initial_location
        self.state = initial_state
        self.agent_type = agent_type
        self.score = 0

    def reset(self):
        self.score = 0

    # agentes deterministicos
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
    
    def reflex_vacuum_random_agent(self):
        cont = 0
        while cont < self.time_steps:
            if self.state == States.DIRTY:
                # self.state = States.CLEAN
                self.score+= rd.randint(0,1) # tornando a ação também aletória

            self.location = Locations(rd.randint(1,2))
            self.state = States(rd.randint(1, 2))
            cont+=1
        return self.score / self.time_steps
    
    # agentes estocásticos 
    def reflex_vacuum_murphy_agent(self):
        cont = 0
        while cont < self.time_steps:
            if cont % 4 == 0 and cont != 0: # Em 25% do tempo, a ação de aspirar o chão não consegue limpá-lo caso este esteja sujo, ou, caso esteja limpo, sujeira é depositada acidentalmente.
                cont+=1
                continue
            # Código repetido do reflex_vacuum_agent()
            elif self.state == States.DIRTY and cont % 10 != 0 and cont != 0: # Sensor de sujeira da a resposta errada em 10% das vezes
                self.state = States.CLEAN
                self.score+=1
            elif self.location == Locations.LEFT:
                self.location = Locations.RIGHT
            elif self.location == Locations.RIGHT:
                self.location = Locations.LEFT

            self.state = States(rd.randint(1, 2))
            cont+=1

        return self.score / self.time_steps
    
    # iterador
    def reflex_vacuum_iterate(self, iterations):
        result = cont = 0
        while cont < iterations:
            match(self.agent_type):
                case AgentType.SIMPLE:
                    result += self.reflex_vacuum_agent()
                case AgentType.RANDOM:
                    result += self.reflex_vacuum_random_agent()
                case AgentType.MURPHY:
                    result += self.reflex_vacuum_murphy_agent()
            self.reset()
            cont+=1

        return result / iterations
    