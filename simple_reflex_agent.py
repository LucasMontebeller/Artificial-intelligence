from vacuum_cleaner import Locations, States, VacuumCleaner, AgentType

def main():

    # definições do agente
    TIME_STEPS = int(1e3)
    # AGENT_TYPE = AgentType.SIMPLE
    AGENT_TYPE = AgentType.RANDOM

    # estados iniciais
    # da para melhorar a lógica em um dicionário de estados
    cleaner_right_dirty = VacuumCleaner(TIME_STEPS, Locations.RIGHT, States.DIRTY, AGENT_TYPE)
    cleaner_right_clean = VacuumCleaner(TIME_STEPS, Locations.RIGHT, States.CLEAN, AGENT_TYPE)
    cleaner_left_dirty = VacuumCleaner(TIME_STEPS, Locations.LEFT, States.DIRTY, AGENT_TYPE)
    cleaner_left_clean = VacuumCleaner(TIME_STEPS, Locations.LEFT, States.CLEAN, AGENT_TYPE)

    results = [
        cleaner_right_dirty.reflex_vacuum_iterate(TIME_STEPS), 
        cleaner_right_clean.reflex_vacuum_iterate(TIME_STEPS),
        cleaner_left_dirty.reflex_vacuum_iterate(TIME_STEPS),
        cleaner_left_clean.reflex_vacuum_iterate(TIME_STEPS)
    ]

    print(f""" Resultados para um agente {AGENT_TYPE.name} com {TIME_STEPS} iterações:
        cleaner_right_dirty => {results[0]} 
        cleaner_right_clean => {results[1]}
        cleaner_left_dirty => {results[2]}
        cleaner_left_clean => {results[3]}""")
    

if __name__ == "__main__":
    main()