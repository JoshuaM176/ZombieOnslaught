import pygame as pg

inp = {"hor": 0,
        "ver": 0,
        "eq": 0,
        "rel": 0,
        "sprint": 1,
        "shooting": 0}

p_inp_map = {pg.K_a: ["hor", -1],
             pg.K_d: ["hor", 1],
             pg.K_w: ["ver", -1],
             pg.K_s: ["ver", 1],
             pg.K_q: ["eq", -1],
             pg.K_e: ["eq", 1],
             pg.K_r: ["rel", 1],
             pg.K_LSHIFT: ["sprint", 1],
             pg.K_SPACE: ["shooting", 1]}

r_inp_map = {pg.K_a: ["hor", 1],
             pg.K_d: ["hor", -1],
             pg.K_w: ["ver", 1],
             pg.K_s: ["ver", -1],
             pg.K_LSHIFT: ["sprint", -1],
             pg.K_SPACE: ["shooting", -1]}