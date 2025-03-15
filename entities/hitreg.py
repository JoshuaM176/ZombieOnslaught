from entities.hitbox import HitBox
from entities.bullets import Bullet

def hitreg(hitbox: HitBox, bullet: Bullet):
    points = hitbox.get()
    if(bullet.x > points[0] and bullet.y > points[1] and bullet.x < points[2] and bullet.y < points[3]):
        return True
    return False