import queue
import pygame as pg
import entities.zombies as ent
from entities.player import Player
from resources.mappings.player_input import inp, p_inp_map, r_inp_map
from registries.zombie_registry import ZombieRegistry
from registries.bullet_registry import TracerRegistry, BulletRegistry
from registries.weapon_registry import WeaponRegistry
from entities.hitreg import hitreg

pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()
running = True
eventQ = queue.Queue()
zombie_registry = ZombieRegistry(pg.sprite.RenderPlain(()))
bullet_registry = BulletRegistry(TracerRegistry(1000, screen), 200)
weapon_registry = WeaponRegistry(pg.sprite.RenderPlain(()))
weapon_registry.load_default_weapons(bullet_registry)
player = Player(screen, weapon_registry, pg.sprite.RenderPlain(()))

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
            zombie_registry.register(ent.Zombie('zombie', 1500, 500))

    #hit register
    bullets = bullet_registry.get()
    zombies = zombie_registry.get()
    for bullet in bullets:
        for zombie in zombies:
            if(hitreg(zombie.hitbox, bullet)):
                zombie.hit(bullet.damage)
                bullet.hit()

    # clear screen
    screen.fill(color=(200,200,200))
    #debug
    #for zombie in zombies:
        #zombie.hitbox.display(screen)
    #player.hitbox.display(screen)
    #render game
    bullet_registry.update()
    player.process(inp)
    zombie_registry.update(screen)
    pg.display.flip()

    #Add events and process end of frame
    zombie_registry.end_of_frame()
    if zombie_registry.isEmpty() == True:
        eventQ.put("NewRound")

    clock.tick(60)


pg.quit()