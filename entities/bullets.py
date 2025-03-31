import math

class Bullet:
    def __init__(self, x: int, y: int, hor: int, ver: int, speed: int, damage: int, head_mult: float, dropoff: float, penetration: float, color, tracer, **_):
        self.x = x
        self.y = y
        mult = speed/math.sqrt(hor**2 + ver**2)
        self.hor = mult*hor
        self.ver = mult*ver
        self.damage = damage
        self.penetration = penetration
        self.dropoff = dropoff * abs(speed)/100
        self.color = color
        self.tracer = tracer
        self.head_mult = head_mult

    def hit(self):
        self.damage *= self.penetration
        self.hor *= 0.7
        self.ver *= 0.7

    def update(self):
        prevX = self.x
        prevY = self.y
        self.x += self.hor
        self.y += self.ver
        self.damage -= self.dropoff
        return prevX, prevY, self.x, self.y, 335, self.color
    
class Tracer:
    
    def __init__(self, sX, sY, eX, eY, vis, color):
        self.sX = sX
        self.sY = sY
        self.eX = eX
        self.eY = eY
        self.vis = vis

    def update(self):
        self.vis -= 150
        if self.vis > 0:
            return (250, 250, 0, self.vis), (self.sX, self.sY), (self.eX, self.eY), 2
        return (250, 250, 0, 0), (self.sX, self.sY), (self.eX, self.eY), 1
        


