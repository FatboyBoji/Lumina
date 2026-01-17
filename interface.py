import pyxel

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16

class Interface_gui:
    def __init__(self):
        self.key_states = {
            pyxel.KEY_W: (False, 11),
            pyxel.KEY_A: (False, 11),
            pyxel.KEY_S: (False, 11),
            pyxel.KEY_D: (False, 11),
        }
        self.btn_colors = {
            pyxel.KEY_W: 11,
            pyxel.KEY_A: 11,
            pyxel.KEY_S: 11,
            pyxel.KEY_D: 11,
        }
        self.border_colors = {
            pyxel.KEY_W: 1,
            pyxel.KEY_A: 1,
            pyxel.KEY_S: 1,
            pyxel.KEY_D: 1,
        }

    def draw(self):
        pyxel.rect(128, 0, TILE_SIZE * 5, TILE_SIZE * 9, 0)
        pyxel.line(129, 2, 129, 129, 2)
        pyxel.line(129, 129, 200, 129, 2)
        self.draw_keys()

    def draw_keys(self):
        key_positions = {
            pyxel.KEY_A: (129 + 16 * 1, 16 * 7),
            pyxel.KEY_W: (129 + 16 * 2, 16 * 6),
            pyxel.KEY_D: (129 + 16 * 3, 16 * 7),
            pyxel.KEY_S: (129 + 16 * 2, 16 * 7),
        }

        for key, (x, y) in key_positions.items():
            self.draw_large_text(x, y, chr(key).upper(), self.btn_colors[key])
            pyxel.rectb(x - 3, y - 3, 16, 16, self.border_colors[key])
            pyxel.pset(x - 3, y - 3, 0)
            pyxel.pset(x - 3, y + 12, 0)
            pyxel.pset(x + 12, y - 3, 0)
            pyxel.pset(x + 12, y + 12, 0)

    def draw_large_text(self, x, y, text, color, scale=2):
        for i, char in enumerate(text):
            char_data = self.get_char_data(char)
            for dy, row in enumerate(char_data):
                for dx, pixel in enumerate(row):
                    if pixel:
                        for sy in range(scale):
                            for sx in range(scale):
                                pyxel.pset(x + dx * scale + sx, y + dy * scale + sy, color)

    def get_char_data(self, char):
        font_data = {
            'W': [
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
            ],
            'A': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
            ],
            'S': [
                [0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
            ],
            'D': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
            ],
        }
        return font_data[char]

    def update(self):
        # Reset all button colors and border colors
        for key in self.btn_colors:
            self.btn_colors[key] = 11
            self.border_colors[key] = 1

        # Check key states and update colors
        for key in self.key_states:
            if pyxel.btn(key):
                print(key)
                self.key_states[key] = (True, 2)
                self.btn_colors[key] = 2
                self.border_colors[key] = 6  # Change border color to 5 when key is pressed
            else:
                self.key_states[key] = (False, 11)
                self.border_colors[key] = 1  # Reset border color to 1 when key is not pressed
