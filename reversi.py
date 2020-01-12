import pygame
from view import RectView
from settings import LENGTH
from model import Player, MinMaxPlayer, MinMaxAlphaBetaPlayer, MCTSPlayer, Game
from time import time

pygame.init()
screen = pygame.display.set_mode((820, 820))


p1 = MinMaxPlayer(0, "p1", 3)
p2 = MCTSPlayer(1, "p2")
# p2 = MinMaxAlphaBetaPlayer(1, "p2", 5)
# p2 = Player(1, "p2")

game = Game(p1, p2)

grid = {}
for i in range(LENGTH):
    for j in range(LENGTH):
        grid[(j, i)] = RectView(j*100, i*100, -1)


screen.fill((91, 66, 49))
for k in grid.keys():
    grid[k].val = game.grid[k]
    grid[k].draw(screen)

start = time()
while True:
    pygame.display.update()
    if not game.is_over:
        game.trigger_move()
        for k in grid.keys():
            grid[k].val = game.grid[k]
            # print(game.grid[k])
            grid[k].draw(screen)
        # grid[move].val = p.player_id
        # grid[move].draw(screen)
        # input()
        score = Game.get_score(game.grid)
        print(f"{game.player1}: {score[0]} | {game.player2}: {score[1]}")
    else:
        end = time()
        print("duration:", (end - start))
        input()
