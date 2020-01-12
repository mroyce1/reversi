import numpy as np
from copy import deepcopy
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef generate_adjacent_moves(np.ndarray grid, neighbours):
    cdef set moves = set()
    cdef int minus_one = -1
    cdef tuple x
    cdef tuple n
    cdef double [:,:] grid_memory_view = grid
    cdef list occupied = list(zip(*np.where(grid >= 0)))
    cdef set all_neighbours = set()
    for x in occupied:
        for n in neighbours[x]:
            all_neighbours.add(n)
    for n in all_neighbours:
        if grid_memory_view[n[0], n[1]] == minus_one:
                moves.add(n)
    return list(moves)


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef apply_move(np.ndarray to_grid, tuple move, int player_id):
    cdef int minus_one = -1
    if to_grid[move] != minus_one:
        return to_grid
    #to_grid[move] = player_id
    cdef int x = move[1]
    cdef int y = move[0]

    cdef double [:,:] grid_memory_view = to_grid

    grid_memory_view[y, x] = player_id

    for i in range(x+1, 8):
        if grid_memory_view[y, i] == minus_one:
            break
        elif grid_memory_view[y, i] == player_id:
            grid_memory_view[y, x:i] = player_id
            break

    for i in range(x-1, -1, -1):
        if grid_memory_view[y, i] == minus_one:
            break
        elif grid_memory_view[y, i] == player_id:
            grid_memory_view[y, i:x] = player_id
            break

    for i in range(y+1, 8):
        if grid_memory_view[i, x] == minus_one:
            break
        elif grid_memory_view[i, x] == player_id:
            grid_memory_view[y:i, x] = player_id
            break

    for i in range(y-1, -1, -1):
        if grid_memory_view[i, x] == minus_one:
            break
        elif grid_memory_view[i, x] == player_id:
            grid_memory_view[i:y, x] = player_id
            break

    return to_grid




cpdef max_move_a_b(int player_id, player, neighbours, np.ndarray grid, int depth, int alpha, int beta):
    possible_moves = generate_adjacent_moves(grid, neighbours)
    if depth == 0 or not possible_moves:
        scores = get_score(grid)
        return scores[player_id] - scores[(player_id + 1) % 2]
    cdef int max_val = alpha
    cdef int val
    cdef int max_depth = player.max_depth
    for m in possible_moves:
        grid_copy = deepcopy(grid)
        grid_copy = apply_move(grid_copy, m, player_id)
        val = min_move_a_b(player_id, player, neighbours, grid_copy, depth - 1, max_val, beta)
        if val > max_val:
            max_val = val
            if depth == max_depth:
                player.best_move = m
            if max_val >= beta:
                break
    return max_val



cdef min_move_a_b(int player_id, player, neighbours, np.ndarray grid, int depth, int alpha, int beta):
    possible_moves = generate_adjacent_moves(grid, neighbours)
    if depth == 0 or not possible_moves:
        scores = get_score(grid)
        return scores[player_id] - scores[(player_id + 1) % 2]
    cdef int min_val = beta
    cdef int val
    for m in possible_moves:
        grid_copy = deepcopy(grid)
        grid_copy = apply_move(grid_copy, m, (player_id+1)%2)
        val = max_move_a_b(player_id, player, neighbours, grid_copy, depth - 1, alpha, min_val)
        if val < min_val:
            min_val = val
            if min_val <= alpha:
                break
    return min_val


cpdef get_score(np.ndarray score_grid):
    cdef int first_player_score = (score_grid == 0).sum()
    cdef int second_player_score = (score_grid == 1).sum()
    return [first_player_score, second_player_score]




cpdef max_move(int player_id, player, neighbours, grid, int depth):
    possible_moves = generate_adjacent_moves(grid, neighbours)
    if depth == 0 or not possible_moves:
        scores = get_score(grid)
        return scores[player_id] - scores[(player_id+1)%2]
    cdef int max_val = -9999876
    cdef int val
    cdef int max_depth = player.max_depth
    for m in possible_moves:
        grid_copy = deepcopy(grid)
        grid_copy = apply_move(grid_copy, m, player_id)
        val = min_move(player_id, player, neighbours, grid_copy, depth - 1)
        if val > max_val:
            max_val = val
            if depth == max_depth:
                player.best_move = m
    return max_val

cdef min_move(int player_id, player, neighbours, grid, int depth):
    possible_moves = generate_adjacent_moves(grid, neighbours)
    if depth == 0 or not possible_moves:
        scores = get_score(grid)
        return scores[player_id] - scores[(player_id+1)%2]
    cdef int min_val = 9999999
    cdef int val
    for m in possible_moves:
        grid_copy = deepcopy(grid)
        grid_copy = apply_move(grid_copy, m, (player_id + 1) % 2)
        val = max_move(player_id, player, neighbours, grid_copy, depth - 1)
        if val < min_val:
            min_val = val
    return min_val