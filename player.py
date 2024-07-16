from typing import Any
# from dataclasses import dataclass
from sprite import Sprite, Rect
import pyxel
import time

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Player(Sprite):
    def __init__(self, idx: int, pos: Rect, img: int, app: Any, col: Rect) -> None:
        super(Player, self).__init__(idx, pos, img, app)
        self.Col = col
        self.score = 0
        self.mana_bar = 1
        self.max_health = 5  # 5 hearts max
        self.current_health = self.max_health * 2
        self.last_damage_time = 0
        self.shot_list = []
        self.last_shot_time = 0
        self.shot_cooldown = 0.5
        self.walking_frames = {
            "x+": [0, 1, 2],  # Frames for walking right
            "x-": [0, 1, 2],  # Frames for walking left
            "y+": [3, 4, 5],  # Frames for walking up
            "y-": [3, 4, 5]  # Frames for walking down
        }
        self.current_frame_index = 0
        self.animation_speed = 0.2  # Time in seconds per frame
        self.last_animation_time = time.time()
        self.is_moving = False
        self.box_edges = []
        self.__init_edges()

    def __init_edges(self) -> None:
        """
        those edges we will use to detect a box and then move that box
        :return: None
        """
        self.box_edges = [
            {"rect": Rect(self.Pos.Location.X + 16, self.Pos.Location.Y, 16, 1), "direction": "right"},
            {"rect": Rect(self.Pos.Location.X, self.Pos.Location.Y + 16, 1, 16), "direction": "down"},
            {"rect": Rect(self.Pos.Location.X, self.Pos.Location.Y - 1, 1, 16), "direction": "up"},
            {"rect": Rect(self.Pos.Location.X - 1, self.Pos.Location.Y, 16, 1), "direction": "left"}
        ]

    def draw(self) -> None:
        if not self.is_moving:
            if self.last_dir in ["y-", "y+"]:
                current_frame = 3
            elif self.last_dir in ["x-", "x+"]:
                current_frame = 0
        if self.is_moving:
            current_frame = self.walking_frames[self.last_dir][self.current_frame_index]
        super(Player, self).draw(current_frame)
        pyxel.rect(0, 128, 128 + 64, 8, 0)  # important here is the black screen, where hp_bar
        # pyxel.rect(128, 0, 64, 128, 0)
        pyxel.text(115, 16 * 8 + 2, f"{self.score}", 6)      # f"score: {self.score}", 6)
        self.draw_hp_bar()
        self.fire_gun()
        self.draw_mana_bar()
        if self.epee is not None and time.time() - self.last_epee < 0.2:
            pass
            # here we used to draw the rect of the attack.
            #  pyxel.rect(self.epee.Location.X, self.epee.Location.Y, self.epee.Size.X, self.epee.Size.Y, 8)
        if self.epee is not None and time.time() - self.last_epee < 0.2:
            self.draw_laser()
        #  self.draw_box_edges()
        #  pyxel.rect(self.Col.Location.X+1.5, self.Col.Location.Y+1.5, self.Col.Size.X, self.Col.Size.Y, 12)

    """def update(self) -> None:
        self.update_mana_bar()"""

    def draw_mana_bar(self):
        pyxel.rect(64, 130, 48 * self.mana_bar, 4, 12)
        pyxel.rectb(64, 130, 48, 4, 13)

    def update_mana_bar(self):
        if self.mana_bar <= 1:
            self.mana_bar += 0.0015
        else:
            self.mana_bar = 1

    def draw_box_edges(self) -> None:
        for edge in self.box_edges:
            pyxel.rect(edge["rect"].Location.X, edge["rect"].Location.Y, edge["rect"].Size.X, edge["rect"].Size.Y, 8)

    def move_edges(self, direction: str) -> None:
        for edge in self.box_edges:
            if direction == "right":
                edge["rect"].Location.X += self.DX
            elif direction == "left":
                edge["rect"].Location.X -= self.DX
            elif direction == "up":
                edge["rect"].Location.Y -= self.DX
            elif direction == "down":
                edge["rect"].Location.Y += self.DX

    def update_edges_position(self) -> None:
        for edge in self.box_edges:
            if edge["direction"] == "right":
                edge["rect"].Location.X = self.Pos.Location.X + 16
                edge["rect"].Location.Y = self.Pos.Location.Y
            elif edge["direction"] == "down":
                edge["rect"].Location.X = self.Pos.Location.X
                edge["rect"].Location.Y = self.Pos.Location.Y + 16
            elif edge["direction"] == "up":
                edge["rect"].Location.X = self.Pos.Location.X
                edge["rect"].Location.Y = self.Pos.Location.Y - 1
            elif edge["direction"] == "left":
                edge["rect"].Location.X = self.Pos.Location.X - 1
                edge["rect"].Location.Y = self.Pos.Location.Y

    def key(self) -> None:
        """
        here we handle the input for the player.
        :return: None
        """
        self.is_moving = False
        current_time = time.time()

        if pyxel.btn(pyxel.KEY_W):  # move up
            self.last_dir = "y+"
            self.move_player(0, -1 * self.DX, "up")

        if pyxel.btn(pyxel.KEY_A):  # move left
            self.last_dir = "x-"
            self.look_direction = +1
            self.move_player(-1 * self.DX, 0, "left")

        if pyxel.btn(pyxel.KEY_D):  # move right
            self.last_dir = "x+"
            self.look_direction = -1
            self.move_player(1 * self.DX, 0, "right")

        if pyxel.btn(pyxel.KEY_S):  # move down
            self.last_dir = "y-"
            self.move_player(0, 1 * self.DX, "down")

        if self.is_moving and current_time - self.last_animation_time >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.walking_frames[self.last_dir])
            self.last_animation_time = current_time
        if pyxel.btn(pyxel.KEY_SPACE):
            self.attack()
        if pyxel.btn(pyxel.KEY_UP):
            self.last_dir = "y+"
        if pyxel.btn(pyxel.KEY_DOWN):
            self.last_dir = "y-"
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.look_direction = -1
            self.last_dir = "x+"
        if pyxel.btn(pyxel.KEY_LEFT):
            self.look_direction = 1
            self.last_dir = "x-"

    def move_player(self, dx: float, dy: float, direction: str) -> None:
        new_x = self.Pos.Location.X + dx
        new_y = self.Pos.Location.Y + dy

        if not self.check_tile_collision(new_x, new_y, direction):
            movable, boxes_hit = self.move_box(direction)

            if movable or not self.box_in_way(new_x, new_y):
                self.Pos.Location.X = new_x
                self.Pos.Location.Y = new_y
                self.Col.Location.X += dx
                self.Col.Location.Y += dy
                self.is_moving = True
                self.move_edges(direction)

    def move_box(self, direction: str) -> tuple[bool, int]:
        """
        we check with the edges what box we are hitting and then move the box
        :param direction:
        :return: tuple[bool, int] -> information if boxes where moved and how many
        """
        boxes_hit = 0
        movable = True

        for box in self.app.Boxes:
            for edge in self.box_edges:
                if edge["direction"] == direction and edge["rect"].intersects_With(box.Pos):
                    boxes_hit += 1
                    box_new_x = box.Pos.Location.X
                    box_new_y = box.Pos.Location.Y

                    if direction == "left":
                        box_new_x -= self.DX
                    elif direction == "right":
                        box_new_x += self.DX
                    elif direction == "up":
                        box_new_y -= self.DX
                    elif direction == "down":
                        box_new_y += self.DX

                    if not self.check_tile_collision(box_new_x, box_new_y, direction) and not self.box_in_way(box_new_x, box_new_y, box):
                        box.Pos.Location.X = box_new_x
                        box.Pos.Location.Y = box_new_y
                    else:
                        movable = False  # If any box can't move, set movable to False

        return movable, boxes_hit  # Return whether all boxes can move and number of boxes hit

    def how_many_boxes_hit(self, direction: Any) -> int:
        """
        :param direction:
        :return: Int -> how many boxes are hit
        """
        count = 0  # Initialize a counter for boxes hit
        for box in self.app.Boxes:
            for edge in self.box_edges:
                if edge["direction"] == direction and edge["rect"].intersects_With(box.Pos):
                    count += 1
        return count

    def box_in_way(self, new_x: float, new_y: float, moving_box=None) -> bool:
        """
        :param new_x:
        :param new_y:
        :param moving_box:
        :return: bool -> True if box is in way, else False
        """
        player_rect = Rect(new_x, new_y, self.Pos.Size.X, self.Pos.Size.Y)
        for box in self.app.Boxes:
            if box != moving_box and box.Pos.intersects_With(player_rect):
                return True
        for potion in self.app.Potions:
            if potion != moving_box and potion.Pos.intersects_With(player_rect):
                return True
        for enemy in self.app.Enemies:
            if enemy != moving_box and enemy.Pos.intersects_With(player_rect):
                return True
        return False

    def draw_hp_bar(self) -> None:
        """
        we draw the hp bar under map on the right sight starting with 5 hearts = 10 hp
        :return: None
        """
        x = 8
        y = 129
        heart_width = 8
        img_bank = 0
        for i in range(self.max_health):
            if self.current_health == 0:
                self.app.GameOver = True
                self.Pos.Location.X = 1 * TILE_SIZE
                self.Pos.Location.Y = 1 * TILE_SIZE
                self.current_health = 10
                self.app.current_room_index = 0
                self.app.new_room = True
            if self.current_health > 10:
                pyxel.blt(x + i * heart_width + 8, y, img_bank, 8, 120, heart_width, heart_width, 0)
            elif self.current_health > i * 2 + 1:
                #  pyxel.blt(x + i * heart_width + 8, y, img_bank, 8, 120, heart_width, heart_width, 0)  # Full heart
                pyxel.blt(x + i * heart_width, y, img_bank, 0, 112, heart_width, heart_width, 0)  # Full heart
            elif self.current_health == i * 2 + 1:
                pyxel.blt(x + i * heart_width, y, img_bank, 8, 112, heart_width, heart_width, 0)  # Half heart
            else:
                pyxel.blt(x + i * heart_width, y, img_bank, 0, 120, heart_width, heart_width, 0)  # Empty heart

    def take_damage(self, amount: int) -> None:
        if self.current_health <= 10:
            self.score -= 5
            self.current_health = max(0, self.current_health - amount)

    def heal(self, amount: int) -> None:
        if self.current_health > 10:
            self.current_health = min(11, self.current_health + amount)
        if self.current_health <= 10:
            self.current_health = min(self.max_health * 2, self.current_health + amount)

    def check_collision_with_enemies(self) -> None:
        current_time = time.time()
        for enemy in self.app.Enemies:
            if self.Pos.intersects_With(enemy.Pos):
                if current_time - self.last_damage_time >= 1:
                    self.take_damage(1)
                    self.last_damage_time = current_time

    def check_collision_with_potion(self) -> None:
        for potion in self.app.Potions[:]:
            if self.Pos.intersects_With(potion.Pos):
                self.heal(3)
                self.app.potion_collected(potion.ID)

    def check_collision_with_treasure(self) -> None:
        self.app.check_collision_with_treasure()

    """Plan for attack(): i want to change it so i can control the direction by the key arrows/ alternative mouse 
    direction c: more dynamic maybe"""

    def attack(self) -> None:
        """
        here we create the attack - Rect for the collision and the effects (kill enemy, etc.)
        :return:None
        """
        scale = 0
        current_time = time.time()
        if self.mana_bar > 0.3 and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            if self.last_dir == "x-" and self.mana_bar > 0.3:  # Left
                self.mana_bar -= 0.3
                scale = 1
                self.epee = Rect(self.Pos.Location.X - self.Pos.Size.X - 16, self.Pos.Location.Y + 6, self.Pos.Size.X / 2, self.Pos.Size.Y + 16)
            elif self.last_dir == "x+" and self.mana_bar > 0.3:  # Right
                self.mana_bar -= 0.3
                scale = 1
                self.epee = Rect(self.Pos.Location.X + self.Pos.Size.X, self.Pos.Location.Y + 6, self.Pos.Size.X / 2, self.Pos.Size.Y + 16)
            elif self.last_dir == "y+" and self.look_direction == 1 and self.mana_bar > 0.1:  # Up, left
                self.mana_bar -= 0.1
                scale = 2
                self.epee = Rect(self.Pos.Location.X, self.Pos.Location.Y - self.Pos.Size.Y, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            elif self.last_dir == "y+" and self.look_direction != 1 and self.mana_bar > 0.1:  # Up, right
                self.mana_bar -= 0.1
                scale = 2
                self.epee = Rect(self.Pos.Location.X + 12, self.Pos.Location.Y - self.Pos.Size.Y, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            elif self.last_dir == "y-" and self.look_direction == 1 and self.mana_bar > 0.1:  # Down, left
                self.mana_bar -= 0.1
                scale = 2
                self.epee = Rect(self.Pos.Location.X, self.Pos.Location.Y + self.Pos.Size.Y - 4, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            elif self.last_dir == "y-" and self.look_direction != 1 and self.mana_bar > 0.1:  # Down, right
                self.mana_bar -= 0.1
                scale = 2
                self.epee = Rect(self.Pos.Location.X + 12, self.Pos.Location.Y + self.Pos.Size.Y - 4, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            self.last_epee = current_time
        self.app.check_enemy_hits(self.epee, scale)

    def draw_laser(self) -> None:
        """
        We draw the laser on the screen with the effects established in attack()
        :return: None
        """
        if self.last_dir == "x+":
            pyxel.blt(self.Pos.Location.X + self.Pos.Size.X, self.Pos.Location.Y + 3, 0, 16, 96, 16, 16, 0)
            pyxel.blt(self.Pos.Location.X + self.Pos.Size.X + 16, self.Pos.Location.Y + 3, 0, 32, 96, 16, 16, 0)
        if self.last_dir == "x-" and self.look_direction == 1:
            pyxel.blt(self.Pos.Location.X - self.Pos.Size.X, self.Pos.Location.Y + 3, 0, 16, 96, -16, 16, 0)
            pyxel.blt(self.Pos.Location.X - 2 * self.Pos.Size.X, self.Pos.Location.Y + 3, 0, 32, 96, -16, 16, 0)
        if self.last_dir == "y-" and self.look_direction == 1:  # Down, left
            pyxel.blt(self.Pos.Location.X - 4, self.Pos.Location.Y + self.Pos.Size.Y - 4, 0, 32, 80, 16, 16, 0)
            pyxel.blt(self.Pos.Location.X - 4, self.Pos.Location.Y + self.Pos.Size.Y - 4 + 16, 0, 32, 80, 16, 16, 0)
        elif self.last_dir == "y-" and self.look_direction != 1:  # Down, right
            pyxel.blt(self.Pos.Location.X + 8, self.Pos.Location.Y + self.Pos.Size.Y - 4, 0, 32, 80, 16, 16, 0)
            pyxel.blt(self.Pos.Location.X + 8, self.Pos.Location.Y + self.Pos.Size.Y - 4 + 16, 0, 32, 80, 16, 16, 0)
        elif self.last_dir == "y+" and self.look_direction == 1:  # Up, left
            pyxel.blt(self.Pos.Location.X - 3, self.Pos.Location.Y - self.Pos.Size.Y / 2 + 2, 0, 32, 80, 16, -16, 0)
            pyxel.blt(self.Pos.Location.X - 3, self.Pos.Location.Y - self.Pos.Size.Y / 2 + 2 - 16, 0, 32, 80, 16, -16, 0)
        elif self.last_dir == "y+" and self.look_direction != 1:  # Up, right
            pyxel.blt(self.Pos.Location.X + 7, self.Pos.Location.Y - self.Pos.Size.Y / 2 + 2, 0, 32, 80, 16, -16, 0)
            pyxel.blt(self.Pos.Location.X + 7, self.Pos.Location.Y - self.Pos.Size.Y / 2 + 2 - 16, 0, 32, 80, 16, -16, 0)

    def fire_gun(self) -> None:
        """
        here we handle drawing and effects of the shots fired in one methode.
        :return: None
        """
        current_time = pyxel.frame_count / 60
        # If the player enters a new room, clear the shot list
        if self.app.new_room:
            self.shot_list = []

        if pyxel.btn(pyxel.KEY_2) and self.mana_bar > 0.2 and current_time - self.last_shot_time >= self.shot_cooldown:
            self.shot_list.append(
                {"direction": self.last_dir, "x": self.Pos.Location.X + 8, "y": self.Pos.Location.Y + 9})
            self.last_shot_time = current_time
            self.mana_bar -= 0.2

        for i in range(len(self.shot_list) - 1, -1, -1):
            shot = self.shot_list[i]

            # Draw the shot
            if 0 <= shot["x"] <= pyxel.width and 0 <= shot["y"] <= pyxel.height:
                pyxel.circb(shot["x"], shot["y"], 3, 8)
                pyxel.blt(shot["x"] - 7, shot["y"] - 7, 0, 16, 48, 16, 16, 0)

            if shot["direction"] == "x+":
                shot["x"] += 1
            elif shot["direction"] == "x-":
                shot["x"] -= 1
            elif shot["direction"] == "y+":
                shot["y"] -= 1
            elif shot["direction"] == "y-":
                shot["y"] += 1

            shot_dmg_value = 3
            if self.app.check_enemy_hits(Rect(shot["x"], shot["y"], 4, 4), shot_dmg_value):
                self.shot_list.pop(i)
                continue

            # Check if the shot is out of bounds
            if shot["x"] < 1 or shot["x"] > 126 or shot["y"] < 2 or shot["y"] > 126:
                self.shot_list.pop(i)
                continue
