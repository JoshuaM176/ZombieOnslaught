import queue
import pygame as pg
from entities.player import Player
from resources.mappings.player_input import inp, p_inp_map, r_inp_map
from registries.zombie_registry import ZombieRegistry
from registries.bullet_registry import TracerRegistry, BulletRegistry
from entities.hitreg import hitreg, hitreg1
from game.ui import UI
from game.game import Game
from screeninfo import get_monitors

screen_info = get_monitors()
pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()
running = True
eventQ = queue.Queue()
ui = UI(screen)
game = Game(ui)
zombie_registry = ZombieRegistry(pg.sprite.RenderPlain(()), ui)
zombie_bullet_registry = BulletRegistry(TracerRegistry(1000, screen), 200)
bullet_registry = BulletRegistry(TracerRegistry(1000, screen), 200)
player = Player(screen, bullet_registry, pg.sprite.RenderPlain(()), ui)

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

    while not eventQ.empty():
        event = eventQ.get()
        if event == "NewRound":
            game.new_wave(zombie_registry, zombie_bullet_registry, *screen.get_size())

    #hit register
    hitreg(zombie_registry, bullet_registry)

    hitreg1([player], zombie_bullet_registry.get())

    # clear screen
    screen.fill(color=(200,200,200))
    #debug
    zombies = zombie_registry.get()
    #for zombie in zombies:
        #zombie.hitbox.display(screen)
        #zombie.head_hitbox.display(screen)
    #player.hitbox.display(screen)
    #render game
    bullet_registry.update()
    zombie_bullet_registry.update()
    player.process(inp)
    zombie_registry.update(screen)
    ui.draw()

    pg.display.flip()

    #Add events and process end of frame
    zombie_registry.end_of_frame()
    if zombie_registry.isEmpty() == True:
        eventQ.put("NewRound")

    clock.tick(60)


pg.quit()