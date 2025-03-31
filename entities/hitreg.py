from entities.hitbox import HitBox
from entities.bullets import Bullet
from entities.entity import Entity
from registries.bullet_registry import BulletRegistry
from registries.zombie_registry import ZombieRegistry

def hitreg(zombie_registry: ZombieRegistry, bullet_registry: BulletRegistry):
    hitreg1(zombie_registry.get(), bullet_registry.get())

def hitreg1(entities: list[Entity], bullets):
    for bullet in bullets:
        for entity in entities:
            if(hitreg2(entity.hitbox, bullet)):
                if(hitreg2(entity.head_hitbox, bullet)):
                    entity.hit(bullet.damage * bullet.head_mult)
                else:
                    entity.hit(bullet.damage)
                bullet.hit()

def hitreg2(hitbox: HitBox, bullet: Bullet):
    points = hitbox.get()
    if(bullet.x > points[0] and bullet.y > points[1] and bullet.x < points[2] and bullet.y < points[3]):
        return True
    return False