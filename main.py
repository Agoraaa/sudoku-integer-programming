from ortools.linear_solver import pywraplp
from sudoku import Sudoku
import time

def add_notequal_const(x, y, solver):
    if (type(x) == int) and (type(y) == int):
        return
    is_bigger = solver.IntVar(0.0, 1.0, '')
    solver.Add(x - y <= -0.5 + is_bigger*20)
    solver.Add(x - y >= 0.5 + (1-is_bigger)*-20)

def add_square_constraints(topleft, table, solver):
    topleft_x, topleft_y = topleft
    cells = []
    for i in range(3):
        for j in range(3):
            cells.append(table[topleft_x + i][topleft_y + j])
    for i in range(len(cells)-1):
        for j in range(i+1, len(cells)):
            add_notequal_const(cells[i], cells[j], solver)

game = Sudoku(3).difficulty(0.75)
decision_vars = []

solver = pywraplp.Solver.CreateSolver("SAT")
if not solver:
    print('Could not create solver')
    exit(1)

game.show()
print('Press enter to start solving')
input()
start_ts = time.time()
width = game.width*3
height = game.height*3

for i in range(width):
    new_row = [0] * width
    for j in range(height):
        if game.board[i][j] is None:
            new_row[j] = solver.IntVar(1.0, width, '')
        else:
            new_row[j] = game.board[i][j]
    decision_vars.append(new_row)

for i in range(game.width):
    for j in range(game.height):
        add_square_constraints((i*3, j*3), decision_vars, solver)
for i in range(width):
    for j in range(height-1):
        for k in range(j +1, height):
            add_notequal_const(decision_vars[i][j], decision_vars[i][k], solver)
            add_notequal_const(decision_vars[j][i], decision_vars[k][i], solver)
            
print(f'Num variables: {solver.NumVariables()}')
print(f'Num constraints: {solver.NumConstraints()}')
solver.Maximize(decision_vars[0][0])
res = solver.Solve()
for row in decision_vars:
    for entry in row:
        if type(entry) == int:
            print(f'{entry} ', end='')
        else:
            print(f'{entry.solution_value():1.0f} ', end='')
    print()
solution_time = time.time() - start_ts
print(f'Solved in {solution_time:0.4f} seconds')