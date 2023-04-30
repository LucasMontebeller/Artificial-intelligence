# Optimization problem using PuLP

import pandas as pd
import os 
from pulp import *
import numpy as np
import locale

locale.setlocale(locale.LC_ALL, '')
locale._override_localeconv = {'mon_thousands_sep': '.'}
DIR_PATH = '~/Downloads'
MAXIMUM_SPEND = 1e8

player_stats = pd.read_csv(os.path.join(DIR_PATH, 'Player_Stats.csv'))
player_salary = pd.read_csv(os.path.join(DIR_PATH, 'Player_Salary.csv'))

# Join and clean data
for p in range(player_salary.shape[0]):
    player_salary['SALARY'][p] = player_salary['SALARY'][p].replace('.', '').replace(',', '.')

stats_salaries = player_stats.merge(player_salary, on='PLAYER')
stats_salaries = stats_salaries.drop(axis=1, columns=['RANK_x', 'RANK_y'])
stats_salaries = stats_salaries.replace(np.nan, 0.0)
stats_salaries['SALARY'] = stats_salaries['SALARY'].astype('float32')

# Preparing
player_vars = LpVariable.dicts("Player", stats_salaries['PLAYER'], lowBound=0.0, upBound=1.0, cat='Continuous')
media_points = (0.6 * stats_salaries['PPG'] + 0.2 * stats_salaries['APG'] + 0.1 * stats_salaries['RPG'] + 0.1 * stats_salaries['BPG'])
project_points = dict(zip(stats_salaries['PLAYER'], media_points))
positions = dict(zip(stats_salaries['PLAYER'], stats_salaries['POS']))
salaries = dict(zip(stats_salaries['PLAYER'], stats_salaries['SALARY']))
pg = [p for p in positions.keys() if positions[p] == 'PG']
sg = [p for p in positions.keys() if positions[p] == 'SG']
sf = [p for p in positions.keys() if positions[p] == 'SF']
pf = [p for p in positions.keys() if positions[p] == 'PF']
c = [p for p in positions.keys() if positions[p] == 'C']

# Solving
total_score = LpProblem('Players_Points_Problem', LpMaximize)
total_score += lpSum([player_vars[i] * project_points[i] for i in player_vars])

# Constraints
total_score += lpSum([salaries[i] * player_vars[i] for i in player_vars]) <= MAXIMUM_SPEND
total_score += lpSum([player_vars[i] for i in pg]) == 2
total_score += lpSum([player_vars[i] for i in sg]) == 2
total_score += lpSum([player_vars[i] for i in sf]) == 2
total_score += lpSum([player_vars[i] for i in pf]) == 2
total_score += lpSum([player_vars[i] for i in c]) == 1

total_score.solve()
selected_players = []
total_salary = 0

if LpStatus[total_score.status] == "Optimal" and total_score.objective.value() > 0:
    for v in total_score.variables():
        if v.varValue > 0:
            selected_players.append(v.name.replace('_', ' ').replace('Player', '').strip())

    print('#' * 100)
    print('Jogadores selecionados:\n')

    for s in selected_players:
        print(f''' {s} ({positions[s]})
            Média (Pontos, rebotes, assistências e bloqueios) : {project_points[s]} | Salário : {salaries[s]}
        ''')
        print('-' * 100)
        total_salary += salaries[s]

    print('#' * 100)
    total_salary = locale.format_string('%.2f', val=total_salary, grouping=True, monetary=True)
    print(f'Total gasto = {total_salary}')
else:
    print(f'Não existe um conjunto de jogadores que atende ao limite de gasto de {MAXIMUM_SPEND}')
