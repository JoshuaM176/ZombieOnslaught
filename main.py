import pygame as pg
import entities.entities as ent
import registries
import queue
from resources.mappings.player_input import inp, p_inp_map, r_inp_map

import registries.zombie_registry

pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()
running = True
eventQ = queue.Queue()
entity_sprites = pg.sprite.RenderPlain(())
zombie_registry = registries.zombie_registry.ZombieRegistry(entity_sprites)
player_sprite = pg.sprite.RenderPlain(())
player = ent.Player()
player_sprite.add(player)


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
            zombie_registry.register(ent.Zombie('zombie.png', ""))

    # render game
    screen.fill(color=(255,255,255))
    entity_sprites.update()
    player_sprite.update(inp)
    entity_sprites.draw(screen)
    player_sprite.draw(screen)
    pg.display.flip()

    #Add events and process end of frame
    zombie_registry.end_of_frame()
    if zombie_registry.isEmpty() == True:
        eventQ.put("NewRound")

    clock.tick(60)


pg.quit()