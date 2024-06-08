import pyxel
import time
import math


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Rect:
    def __init__(self, x, y, height, width):
        self.Location = Point(x, y)
        self.Size = Point(width, height)

    def intersects_With(self, rect):
        sw = self.Size.X / 2  
        sh = self.Size.Y / 2 
        rw = rect.Size.X / 2
        rh = rect.Size.Y / 2
        return (abs((self.Location.X + sw) - (rect.Location.X + rw)) < abs(sw + rw) and  
                abs((self.Location.Y + sh) - (rect.Location.Y + rh)) < abs(sh + rh))


class Sprite:
    def __init__(self, idx, pos, img, app):
        self.Idx = idx
        self.Pos = pos
        self.IMG = img
        self.DX = 0.5 * 2
        self.look_direction = 1
        self.moving_animation_num = 0
        self.current_room_index = 0
        self.tile_wall = [ (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 2), (5, 3), (5, 4), (5, 7)]
        self.tile_boxes = [ (4,0), (4,1), (5,0), (5,1) ]
        self.app = app
        self.last_attack_time = 0
        self.attack_cooldown = 0.4
        self.fired_shoot = None
        self.last_epee = 0
        self.epee = None
        self.last_dir = "y-"

    def draw(self, frame_index):
        pyxel.blt(
            self.Pos.Location.X,
            self.Pos.Location.Y,
            self.IMG,
            (self.Idx + frame_index & 31) * self.Pos.Size.X,
            (self.Idx + frame_index >> 5) * self.Pos.Size.Y,
            self.look_direction * self.Pos.Size.X,
            self.Pos.Size.Y, 0
        )
        #pyxel.blt(16-4,32,0,32,80,16,16,0)            #32,72