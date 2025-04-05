import pygame as pg

from resources.mappings.player_input import inp, p_inp_map, r_inp_map
from game.game import Game
from screeninfo import get_monitors

screen_info = get_monitors()
pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()
running = True

game = Game(screen)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if p_inp_map.get(event.key):
                inp[p_inp_map[event.key][0]] += p_inp_map[event.key][1]
        if event.type == pg.KEYUP:
            if r_inp_map.get(event.key):
                inp[r_inp_map[event.key][0]] += r_inp_map[event.key][1]
    #debug
    #zombies = zombie_registry.get()
    #for zombie in zombies:
        #zombie.hitbox.display(screen)
        #zombie.head_hitbox.display(screen)
    #player.hitbox.display(screen)
    #render game
    screen.fill(color=(200,200,200))
    game.player_input(inp)
    game.update()
    pg.display.flip()
    clock.tick(60)


pg.quit()