import numpy as np
import random
from collections import defaultdict
from queue import PriorityQueue
from copy import deepcopy
from settings import LENGTH
import sys
import compiled
# from scipy.ndimage.interpolation import shift

class Player(object):

    def __init__(self, player_id, name):
        self.name = name
        self.player_id = player_id
        self.player_type = "default"

    def get_move(self, grid):
        possible_moves = list(zip(*np.where(grid == -1)))
        max_score = -1
        max_move = None
        for m in possible_moves:
            grid_copy = deepcopy(grid)
            # grid_copy = Game.apply_move(grid_copy, m, self.player_id)
            grid_copy = compiled.apply_move(grid_copy, m, self.player_id)
            score = Game.get_score(grid_copy)[self.player_id]
            if score > max_score:
                max_score = score
                max_move = m
        return max_move

    def get_random_move(self, grid):
        free = np.where(grid == -1)
        rdm = random.randint(0, len(free[0])-1)
        return (free[0][rdm], free[1][rdm])

    def __repr__(self):
        return f"{self.name} ({self.player_type})"

    # def generate_adjacent_moves(self, grid):
    #     moves = []
    #     checked = set()
    #     for i in range(LENGTH):
    #         for j in range(LENGTH):
    #             if (i, j) in checked:
    #                 continue
    #             checked.add((i, j))
    #             if any(grid[x] >= 0 for x in Game.neighbours[(i, j)]):
    #                 moves.append((i, j))
    #                 continue
    #             # for n in Game.neighbours[(i, j)]:
    #             #     if grid[n] >= 0:
    #             #         moves.append((i, j))

    #     return moves

    def generate_adjacent_moves(self, grid):
        moves = set()
        # checked = set()
        # copy_left = deepcopy(grid)
        # copy_right = deepcopy(grid)
        # copy_up = deepcopy(grid)
        # copy_down = deepcopy(grid)
        # copy_left = shift(copy_left, [-1, 0, 0, 0], cval=-1)
        occupied = list(zip(*np.where(grid >= 0)))
        for x in occupied:
            for n in Game.neighbours[x]:
                if grid[n] == -1:
                    moves.add(n)
        # print(occupied)
        # return list(set())
        return list(moves)


class MinMaxPlayer(Player):

    def __init__(self, player_id, name, max_depth):
        super().__init__(player_id, name)
        self.best_move = None
        self.max_depth = max_depth
        self.player_type = "minmax"

    def get_move(self, grid):
        # self.max_move(grid, self.max_depth)
        compiled.max_move(self.player_id, self, Game.neighbours, grid, self.max_depth)
        return self.best_move

    def max_move(self, grid, depth):
        # possible_moves = list(zip(*np.where(grid == -1)))
        # possible_moves = self.generate_adjacent_moves(grid)
        possible_moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        if depth == 0 or not possible_moves:
            scores = Game.get_score(grid)
            return scores[self.player_id] - scores[(self.player_id+1)%2]
        max_val = float('-inf')
        for m in possible_moves:
            grid_copy = deepcopy(grid)
            # grid_copy = Game.apply_move(grid_copy, m, self.player_id)
            grid_copy = compiled.apply_move(grid_copy, m, self.player_id)
            val = self.min_move(grid_copy, depth - 1)
            if val > max_val:
                max_val = val
                if depth == self.max_depth:
                    self.best_move = m
        return max_val

    def min_move(self, grid, depth):
        # possible_moves = list(zip(*np.where(grid == -1)))
        # possible_moves = self.generate_adjacent_moves(grid)
        possible_moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        if depth == 0 or not possible_moves:
            scores = Game.get_score(grid)
            return scores[self.player_id] - scores[(self.player_id+1)%2]
        min_val = float('inf')
        for m in possible_moves:
            grid_copy = deepcopy(grid)
            grid_copy = compiled.apply_move(grid_copy, m, (self.player_id + 1) % 2)
            val = self.max_move(grid_copy, depth - 1)
            if val < min_val:
                min_val = val
        return min_val


class MinMaxAlphaBetaPlayer(MinMaxPlayer):

    def __init__(self, player_id, name, max_depth):
        super().__init__(player_id, name, max_depth)
        self.player_type = "minmax_a_b"


    def get_move(self, grid):
        # self.max_move_a_b(grid, self.max_depth, float('-inf'), float('inf'))
        compiled.max_move_a_b(self.player_id, self, Game.neighbours, grid, self.max_depth, -36775807, 36775807)
        return self.best_move

    def max_move_a_b(self, grid, depth, alpha, beta):
        # possible_moves = list(zip(*np.where(grid == -1)))
        # possible_moves = self.generate_adjacent_moves(grid)
        possible_moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        if depth == 0 or not possible_moves:
            scores = Game.get_score(grid)
            return scores[self.player_id] - scores[(self.player_id + 1) % 2]
        max_val = alpha
        for m in possible_moves:
            grid_copy = deepcopy(grid)
            # grid_copy = Game.apply_move(grid_copy, m, self.player_id)
            grid_copy = compiled.apply_move(grid_copy, m, self.player_id)
            val = self.min_move_a_b(grid_copy, depth - 1, max_val, beta)
            if val > max_val:
                max_val = val
                if depth == self.max_depth:
                    self.best_move = m
                if max_val >= beta:
                    break
        return max_val

    def min_move_a_b(self, grid, depth, alpha, beta):
        # possible_moves = list(zip(*np.where(grid == -1)))
        # possible_moves = self.generate_adjacent_moves(grid)
        possible_moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        if depth == 0 or not possible_moves:
            scores = Game.get_score(grid)
            return scores[self.player_id] - scores[(self.player_id + 1) % 2]
        min_val = beta
        for m in possible_moves:
            grid_copy = deepcopy(grid)
            # grid_copy = Game.apply_move(grid_copy, m, (self.player_id+1)%2)
            grid_copy = compiled.apply_move(grid_copy, m, (self.player_id+1)%2)
            val = self.max_move_a_b(grid_copy, depth - 1, alpha, min_val)
            if val < min_val:
                min_val = val
                if min_val <= alpha:
                    break
        return min_val

class MCTSNode(object):
    exploration_weight = 1.44

    def __init__(self, father, grid, move, player_id):
        self.father = father
        self.move = move
        if move is None:
            self.grid = grid
        else:
            grid_copy = deepcopy(grid)
            self.grid = compiled.apply_move(grid_copy, move, player_id)
        self.moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        self.grid = grid
        self.uct = 0.0
        self.visits = 0.0
        self.wins = 0.0
        self.won = 0.0
        self.children = []
        self.player_id = player_id




    def expand(self, depth):
        self.visits += 1
        if not self.moves:
            self.select_child(depth)
            return
        rdm = random.randint(0, len(self.moves) - 1)
        m = self.moves.pop(rdm)
        child_node = MCTSNode(self, self.grid, m, (self.player_id + 1) % 2)
        child_node.visits += 1
        self.children.append(child_node)
        score = compiled.get_score(child_node.grid)
        # score = score[self.player_id] - score[child_node.player_id]
        # score = score[1] - score[0]
        score = 1.0 if score[child_node.player_id] > score[self.player_id] else 0.0
        child_node.propagate(child_node.player_id, score)



    def select_child(self, depth):
        # print(depth)
        if not self.children:
            self.propagate(-2, self.won)
            return
        max(self.children, key=lambda x: x.uct).expand(depth+1)


    def propagate(self, p_id, val):
        if p_id != -2:
            self.won = val
        fath = self
        while fath != None:
            # print(fath)
            # fath.wins += self.won if self.player_id == fath.player_id else (1-self.won)
            # print(self.won)
            # fath.wins += self.won if self.player_id == fath.player_id else 0
            fath.wins += self.won if p_id == fath.player_id else 0
            for c in fath.children:
                c.uct = c.wins / c.visits + MCTSNode.exploration_weight * np.sqrt((np.log(fath.visits) / c.visits))
            fath = fath.father

    def __repr__(self):
        return f"uct: {self.uct}  |  visits: {self.visits}  |  wins: {self.wins}\n"


class MCTSPlayer(Player):

    def __init__(self, player_id, name):
        super().__init__(player_id, name)
        self.best_move = None
        self.player_type = "mcts"

    def get_move(self, grid):
        moves = compiled.generate_adjacent_moves(grid, Game.neighbours)
        top = MCTSNode(None, grid, None, self.player_id)
        max_index = 0
        max_visits = -1000
        for i in range(50000):
            top.expand(0)
        # move_node = max(top.children, key=lambda x: x.visits/x.wins)
        move_node = max(top.children, key=lambda x: x.visits)
        print("playing: ", move_node)
        print(top.children)
        return move_node.move
        # for i, c in enumerate(top.children):
        #     if c.visits > max_visits:
        #         max_visits = c.visits
        #         max_index = i
        # print(top.children)
        # return moves[max_index]
        # return moves.index(max(top.children, key=lambda x: x.visits))


class Game(object):

    @staticmethod
    def generate_neighbours():
        neighbours = defaultdict(set)
        shifts = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for i in range(LENGTH):
            for j in range(LENGTH):
                for s in shifts:
                    shifted_x = i + s[0]
                    shifted_y = j + s[1]
                    if shifted_x >= 0 and shifted_x < LENGTH and shifted_y >= 0 and shifted_y < LENGTH:
                        neighbours[(i, j)].add((shifted_x, shifted_y))
        return neighbours

    neighbours = generate_neighbours.__func__()

    def __init__(self, p1, p2):
        self.player1 = p1
        self.player2 = p2
        self.active_player, self.inactive_player = p1, p2
        self.grid = np.empty(shape = (LENGTH, LENGTH))
        self.grid.fill(-1)
        self.grid[(4,4)] = 0
        self.grid[(3,3)] = 0
        self.grid[(4,3)] = 1
        self.grid[(3,4)] = 1

    def switch_active(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player


    def trigger_move(self):
        move = self.active_player.get_move(self.grid)
        # self.grid[move] = self.active_player.player_id
        # print("move", move)
        # self.grid = Game.apply_move(self.grid, move, self.active_player.player_id)
        self.grid = compiled.apply_move(self.grid, move, self.active_player.player_id)
        # print(self.grid)
        self.switch_active()

    @property
    def is_over(self):
        # return len(np.where(self.grid == -1)[0]) == 0
        return (self.grid == -1).sum() == 0


    @staticmethod
    def get_score(score_grid):
        # first_player_score = len((np.where(score_grid) == 0)[0])
        first_player_score = (score_grid == 0).sum()
        # second_player_score = len((np.where(score_grid) == 1)[0])
        second_player_score = (score_grid == 1).sum()
        return [first_player_score, second_player_score]


    @staticmethod
    def apply_move(to_grid, move, player_id):
        if to_grid[move] != -1:
            return to_grid
        to_grid[move] = player_id
        x = move[1]
        y = move[0]

        for i in range(x+1, 8):
            if to_grid[(y, i)] == -1:
                break
            elif to_grid[(y, i)] == player_id:
                to_grid[y, x:i] = player_id
                break

        for i in range(x-1, -1, -1):
            if to_grid[(y, i)] == -1:
                break
            elif to_grid[(y, i)] == player_id:
                to_grid[y, i:x] = player_id
                break

        for i in range(y+1, 8):
            if to_grid[(i, x)] == -1:
                break
            elif to_grid[(i, x)] == player_id:
                to_grid[y:i, x] = player_id
                break

        for i in range(y-1, -1, -1):
            if to_grid[(i, x)] == -1:
                break
            elif to_grid[(i, x)] == player_id:
                to_grid[i:y, x] = player_id
                break

        return to_grid
