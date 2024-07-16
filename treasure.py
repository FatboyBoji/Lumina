from sprite import Sprite
import pyxel

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Treasure(Sprite):
    def __init__(self, idx, pos, img, treasure_id, app):
        super(Treasure, self).__init__(idx, pos, img, app)
        self.ID = treasure_id
        self.collected = False
        self.opening = False
        self.opened = False
        self.interaction = False

    """def draw(self):
        super(Treasure, self).draw(0)"""

    def draw(self):
        if self.opening:
            self.draw_opening_animation()
        if self.interaction:
            self.draw_interaction_popup()
        if self.opened:
            self.draw_opened_treasure()
        else:
            super(Treasure, self).draw(0)

    def draw_opening_animation(self):
        # Add your animation logic here
        pass

    def draw_opened_treasure(self):
        pyxel.blt(self.Pos.Location.X, self.Pos.Location.Y, 0, 0, 128, TILE_SIZE, TILE_SIZE)

    def draw_interaction_popup(self):
        pyxel.blt(2*16, 2*16, 1,  0, 0, 64, 64)
        pyxel.text(5*8 - 2, 5*8, "Open Treasure", 4)
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        pyxel.text(45, 55, "[O] Open", 2)
        if 45 < mouse_x < 84 and 55 < mouse_y < 64:
            pyxel.rectb(43, 53, 44, 10, 3)
            pyxel.text(45, 55, "[O] Open", 8)
        pyxel.text(45, 64, "[I] Ignore", 2)
        if 45 < mouse_x < 84 and 63 < mouse_y < 69:
            pyxel.rectb(43, 62, 44, 9, 3)
            pyxel.text(45, 64, "[I] Ignore", 8)

    def hit_player(self, pos):
        self.interaction = True

    def open(self):
        self.collected = True
        self.opening = True
        self.interaction = False
        self.opened = True