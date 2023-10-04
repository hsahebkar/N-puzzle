import numpy as np

def count_linear_conflicts(board, goal):
    conflicts = 0
    size_x, size_y = board.shape

    for i in range(size_x):
        for j in range(size_y):
            tile = board[i, j]

            if tile == 0:
                continue

            goal_i, goal_j = np.where(goal == tile)

            if i == goal_i:
                row = board[i, :]
                goal_row = goal[i, :]

                # Check for conflicts in the row
                for k in range(j + 1, size_y):
                    if row[k] < tile and goal_row[k] > tile:
                        conflicts += 1

            if j == goal_j:
                column = board[:, j]
                goal_column = goal[:, j]

                # Check for conflicts in the column
                for k in range(i + 1, size_x):
                    if column[k] < tile and goal_column[k] > tile:
                        conflicts += 1

    return conflicts


def Heuristic(board, Final):
    Places = Generate_heuristic_table(Final)
    x_size, y_size = board.shape
    correct, total = 0, 0
    for i in range(x_size):
        for j in range(y_size):
            res = sum(abs(value1 - value2) for value1, value2 in zip((i, j), Places[board[i, j]]))
            total += res
            if res == 0:
                correct += 1
    return len(Places) == correct, 0.5 * total + count_linear_conflicts(board, Final) * 0.5


def Generate_heuristic_table(Init_Board):
    Placement = {}
    size = Init_Board.shape
    for i in range(size[0]):
        for j in range(size[1]):
            Placement[Init_Board[i, j]] = (i, j)
    return Placement
