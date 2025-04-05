import pygame as pg

class UI:

    def __init__(self, screen: pg.display):
        self.screen = screen
        self.render_plain = pg.sprite.RenderPlain
        self.properties = {"player": {}, "zombies": [{}], "weapon": {}, "game": {"wave": 0}}

    def send(self, values: dict):
        self.properties = self.update(self.properties, values)

    def remove(self):
        pass

    def update(self, data: dict, new_data: dict):
        for key, value in new_data.items():
            if type(data.get(key)) == dict and new_data.get(key) is not None:
                self.update(data[key], new_data[key])
            else:
                data[key] = value
        return data
    
    def draw(self):
        font = pg.font.Font(pg.font.get_default_font(), 20)
        ##Player
        player = self.properties["player"]
        max_health = player["max_health"]
        health = player["health"]
        x = player["x"] + 13
        y = player["y"]
        pg.draw.rect(self.screen, (0,255,0), (x, y-10, 100*health/max_health, 20))
        pg.draw.rect(self.screen, (0,0,0), (x, y-10, 100, 20), 1)
        text = str(max(round(health), 0))
        text = font.render(text, True, (0,0,0))
        text_rect = text.get_rect(center = (x + 50, y))
        self.screen.blit(text, text_rect)
        ##Zombies
        for zombie in self.properties["zombies"]:
            max_health = zombie["max_health"]
            health = zombie["health"]
            x = zombie["x"]+zombie["shiftX"]
            y = zombie["y"]
            pg.draw.rect(self.screen, (0,255,0), (x, y-10, 100*health/max_health, 20))
            pg.draw.rect(self.screen, (0,0,0), (x, y-10, 100, 20), 1)
            text = str(max(round(health), 0))
            text = font.render(text, True, (0,0,0))
            text_rect = text.get_rect(center = (x + 50, y))
            self.screen.blit(text, text_rect)
        ##UI
        pg.draw.rect(self.screen, (200, 255, 200), (0, self.screen.get_height()-250, self.screen.get_width(), 250))
        ##Weapons
        font = pg.font.Font(pg.font.get_default_font(), 75)
        weapon = self.properties["weapon"]
        bullets = weapon["bullets"]
        max_bullets = weapon["max_bullets"]
        max_mags = weapon["max_mags"]
        mags = weapon["mags"]
        name = weapon["name"]

        x = self.screen.get_width()
        y = self.screen.get_height()
        text = str(f"{bullets}/{max_bullets}")
        text = font.render(text, True, (0,0,0))
        self.screen.blit(text, (50, y-125))
        font = pg.font.Font(pg.font.get_default_font(), 25)
        text = str(f"{mags}/{max_mags}")
        text = font.render(text, True, (0,0,0))
        self.screen.blit(text, (50, y-50))
        text = str(name)
        text = font.render(text, True, (0,0,0))
        self.screen.blit(text, (50, y-150))
        ##Round
        font = pg.font.Font(pg.font.get_default_font(), 40)
        wave = self.properties["game"]["wave"]
        text = str(f"WAVE: {wave}")
        text = font.render(text, True, (0,0,0))
        text_rect = text.get_rect(center = (x/2, y-225))
        self.screen.blit(text, text_rect)
        ##Money
        font = pg.font.Font(pg.font.get_default_font(), 20)
        money = self.properties["game"]["money"]
        text = str(f"${money}")
        text = font.render(text, True, (0,0,0))
        text_rect = text.get_rect(topright=(x-50, y-225))
        self.screen.blit(text, text_rect)


        