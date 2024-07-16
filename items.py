from sprite import Sprite
import pyxel

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Potion(Sprite):
    def __init__(self, idx, pos, img, potion_id, app):
        super(Potion, self).__init__(idx, pos, img, app)
        self.ID = potion_id
        self.collected = False

    def draw(self):
        super(Potion, self).draw(0)


class Grass(Sprite):
    def __init__(self, idx, pos, img, app):
        super(Grass, self).__init__(idx, pos, img, app)

    def draw(self):
        super(Grass, self).draw(0)


class Box(Sprite):
    def __init__(self, idx, pos, img, box_id, app):
        super(Box, self).__init__(idx, pos, img, app)
        self.ID = box_id
        self.moved = False  # Assume we track if the box has been moved

    def draw(self):
        super(Box, self).draw(0)

    def save_position(self):
        return self.Pos.Location.X / TILE_SIZE, self.Pos.Location.Y / TILE_SIZE

    def load_position(self, position):
        self.Pos.Location.X, self.Pos.Location.Y = position[0] * TILE_SIZE, position[1] * TILE_SIZE


"""
sprite:
    maybe we change sprite, because it has to many attributes of player and other classes.

portal:
    want to add the entity portal. 
    should have different attributes, 

world

movement of enemy

Bugfixes:
    shots fired - new.room = True
    walk collision should be fixed or changed

"""
