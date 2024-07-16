import pyxel
from typing import Tuple
import math

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Point:
    def __init__(self, x, y) -> None:
        self.X = x
        self.Y = y


class Rect:
    def __init__(self, x, y, height, width) -> None:
        self.Location = Point(x, y)
        self.Size = Point(width, height)

    def intersects_With(self, rect) -> bool:
        """
        if two tile overlap this return True
        :param rect:
        :return: bool
        """
        sw = self.Size.X / 2
        sh = self.Size.Y / 2
        rw = rect.Size.X / 2
        rh = rect.Size.Y / 2
        return (abs((self.Location.X + sw) - (rect.Location.X + rw)) < abs(sw + rw) and
                abs((self.Location.Y + sh) - (rect.Location.Y + rh)) < abs(sh + rh))


class Sprite:
    def __init__(self, idx, pos, img, app) -> None:
        self.Idx = idx
        self.Pos = pos
        self.IMG = img
        self.DX = 0.5 * 2

        self.look_direction = 1
        self.current_room_index = 0
        self.tile_wall = [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 2), (5, 3), (5, 4), (5, 7)]
        self.tile_boxes = [(4, 0), (4, 1), (5, 0), (5, 1)]
        self.app = app
        self.last_attack_time = 0
        self.attack_cooldown = 0.4
        self.fired_shoot = None
        self.last_epee = 0
        self.epee = None
        self.last_dir: str = "y-"

    def draw(self, frame_index) -> None:
        """
        here we draw all entities
        :param frame_index:
        :return:
        """
        pyxel.blt(
            self.Pos.Location.X,
            self.Pos.Location.Y,
            self.IMG,
            (self.Idx + frame_index & 31) * self.Pos.Size.X,
            (self.Idx + frame_index >> 5) * self.Pos.Size.Y,
            self.look_direction * self.Pos.Size.X,
            self.Pos.Size.Y, 0
        )
        #  pyxel.blt(16-4,32,0,32,80,16,16,0)            #32,72

    def get_tile(self, tile_x: int, tile_y: int) -> Tuple[int, int]:
        offset_x = self.app.room_coordinates[self.app.current_room_index][0]
        offset_y = self.app.room_coordinates[self.app.current_room_index][1]
        return pyxel.tilemaps[0].pget(tile_x + offset_x, tile_y + offset_y)

    def check_tile_collision(self, new_x: float, new_y: float, direction: str) -> bool:
        """
        here we check if a tile is colliding with another tile. based on three tiles. upper_middle_down_tile
        :param new_x:
        :param new_y:
        :param direction:
        :return: bool
        """
        if direction == "left":
            tile_x = math.floor(new_x / TILE_SIZE * 2)
            tile_y = math.floor(new_y / TILE_SIZE * 2)
            tile_x2 = tile_x
            tile_y2 = math.ceil(new_y / TILE_SIZE * 2 + 1)
        elif direction == "right":
            tile_x = math.ceil(new_x / TILE_SIZE * 2 + 1)
            tile_y = math.floor(new_y / TILE_SIZE * 2)
            tile_x2 = tile_x
            tile_y2 = math.ceil(new_y / TILE_SIZE * 2 + 1)
        elif direction == "up":
            tile_x = math.floor(new_x / TILE_SIZE * 2)
            tile_y = math.floor(new_y / TILE_SIZE * 2)
            tile_x2 = math.ceil(new_x / TILE_SIZE * 2 + 1)
            tile_y2 = tile_y
        elif direction == "down":
            tile_x = math.floor(new_x / TILE_SIZE * 2)
            tile_y = math.ceil(new_y / TILE_SIZE * 2 + 1)
            tile_x2 = math.ceil(new_x / TILE_SIZE * 2 + 1)
            tile_y2 = tile_y

        mid_tile_x = (tile_x + tile_x2) // 2
        mid_tile_y = (tile_y + tile_y2) // 2

        tile = self.get_tile(tile_x, tile_y)
        tile2 = self.get_tile(tile_x2, tile_y2)
        tile3 = self.get_tile(mid_tile_x, mid_tile_y)

        return tile in self.tile_wall or tile2 in self.tile_wall or tile3 in self.tile_wall
