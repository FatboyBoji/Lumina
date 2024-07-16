"""Lumina"""
"""i love u too"""
"""Project started in 2024 by Esriges Ri and Bogigis Dar <3"""

import pyxel
from player import Player
from enemy import Enemy
from items import Potion, Grass, Box
from treasure import Treasure
from sprite import Rect
from interface import Interface_gui

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class App:
    def __init__(self) -> None:
        """
        initialising all main variables
        """
        pyxel.init(TILE_SIZE * MAP_WIDTH + 16*5, TILE_SIZE * MAP_LENGTH + 8, title="Lumina", display_scale=6, fps=60)
        pyxel.load("main.py.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.mouse(True)

        self.menu = True
        self.new_room = True
        self.room_coordinates = [(0, 0), (16, 0), (32, 0), (48, 0), (64, 0)]
        self.current_room_index = 0
        self.aim_direction = "R"
        self.visited_P = set()  #no need for now but here I am handling the items, enemies spawns in a room
        self.enemy_states = {}
        self.enemy_positions = {}
        self.potion_states = {}
        self.treasure_states = {}
        self.box_positions = {}  # Dictionary to store box positions
        self.entity_spawners = {
            'Enemies': self.spawn_enemies,
            'Boxes': self.spawn_boxes,
            'Grass': self.spawn_grass,
            'Treasure': self.spawn_treasure,
            'Potions': self.spawn_potion,
        }
        self.GameOver = False
        self.game_Start = False
        self.hp_bar = 6

        # Variables for blinking and color-changing text
        self.frame_count = 0
        self.text_visible = True
        self.text_color = 6
        self.colors = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.start()
        self.initialize_entities()
        self.interacting_treasure = None  # Test Treasure
        self.interface_gui = Interface_gui()
        pyxel.run(self.update, self.draw)

    def start(self) -> None:
        """
        initialise the main Player
        :return: None
        """
        self.size_obj = 1
        self.PlayerM = Player(0, Rect(1 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE * self.size_obj, TILE_SIZE * self.size_obj), 0, self,
                              Rect(20, 23, 5, 5))

    def initialize_entities(self) -> None:
        """
        initialise the entities, later can add extra entities here
        :return: None
        """
        self.Enemies = []
        self.Boxes = []
        self.Grass = []
        self.Treasure = []
        self.Potions = []
        self.spawn_entities()

    def update(self) -> None:
        """
        this loop is updating constantly everything about the game
        :return: None
        """
        if self.GameOver:
            self.menu = True
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_RETURN):
            pyxel.stop()  # Stop the menu music
            self.menu = False
            self.game_Start = True
        if self.game_Start:
            if self.interacting_treasure:
                self.handle_treasure_interaction()
            else:
                self.PlayerM.key()
                self.room_change()
                self.PlayerM.check_collision_with_enemies()
                self.PlayerM.check_collision_with_potion()
                self.PlayerM.check_collision_with_treasure()
                self.PlayerM.update_mana_bar()
                self.update_enemies()
                self.interface_gui.update()

        # Increment frame count and update text state
        self.frame_count += 2
        if self.frame_count % 30 == 0:  # Change visibility every 30 frames
            self.text_visible = not self.text_visible
        if self.frame_count % 60 == 0:  # Change color every 60 frames
            self.text_color = self.colors[(self.colors.index(self.text_color) + 1) % len(self.colors)]

    def draw(self) -> None:
        """
        here we visualise everything on the screen
        :return: None
        """
        if self.menu:
            self.GameOver = False
            self.game_Start = False
            self.new_room = True
            self.current_room_index = 0
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 128 * 2, 128, 128)
            pyxel.text(16 * 1.5, 16 * 4, "Press ENTER to play", 8)
            if self.text_visible:
                pyxel.text(16 * 1.5, 16 * 4, "      ENTER        ", self.text_color)
        else:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, self.room_coordinates[self.current_room_index][0] * 8, self.room_coordinates[self.current_room_index][1] * 8, pyxel.width, pyxel.height)
            self.game_Start = True
            if self.new_room:
                self.spawn_entities()
            for entity_list in [self.Grass, self.Potions, self.Treasure, self.Enemies, self.Boxes]:
                for entity in entity_list:
                    entity.draw()
            self.PlayerM.draw()

            # Draw interaction popup if interacting with a treasure
            if self.interacting_treasure:
                self.interacting_treasure.draw_interaction_popup()
            #  pyxel.line(16*1,16,16*3,16,8)

            # Draw the interface overlay
            self.interface_gui.draw()

    def room_change(self) -> None:
        """
        here we handle the room logic, item and enemy updating: position or existence
        :return: None
        """
        player_x = self.PlayerM.Pos.Location.X
        player_y = self.PlayerM.Pos.Location.Y
        self.new_room = False

        if player_x >= pyxel.width - 16*5:  # 128 - 1
            self.save_box_positions()  # Save box positions before changing room
            self.save_enemy_positions()
            self.current_room_index = min(self.current_room_index + 1, len(self.room_coordinates) - 1)
            self.PlayerM.Pos.Location.X = 0
            self.new_room = True

        elif player_x < -11 and player_y <= 32:
            self.save_box_positions()  # Save box positions before changing room
            self.save_enemy_positions()
            self.current_room_index = max(self.current_room_index - 1, 0)
            self.PlayerM.Pos.Location.X = pyxel.width - TILE_SIZE - 16*5
            self.new_room = True

        if self.new_room:
            self.spawn_entities()
            self.PlayerM.update_edges_position()
            self.load_box_positions()  # Load box positions when entering a new room
            self.load_enemy_positions()

    """we spawn everything now"""

    def spawn_entities(self) -> None:
        """
        we call all functions below to spawn all entities
        :return: None
        """
        for spawn_method in self.entity_spawners.values():
            spawn_method()

    def spawn_potion(self) -> None:
        """
        we spawn a new potion with a specifc ID
        :return: None
        """
        self.Potions = []
        potion_spawn_points = {
            0: [(3, 5)],
            1: [],
            2: [(6, 6)],
            3: [],
            4: []
        }
        if self.current_room_index in potion_spawn_points:
            if self.current_room_index not in self.potion_states:
                self.potion_states[self.current_room_index] = [True] * len(potion_spawn_points[self.current_room_index])
            for i, (x, y) in enumerate(potion_spawn_points[self.current_room_index]):
                if self.potion_states[self.current_room_index][i]:
                    self.Potions.append(
                        Potion(4 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))

    def potion_collected(self, potion_id: int) -> None:
        """
        here we update the state of the potions, and according to that we handle their visuals
        :param potion_id:
        :return: None
        """
        room_index = self.current_room_index
        if room_index in self.potion_states and potion_id < len(self.potion_states[room_index]):
            self.potion_states[room_index][potion_id] = False

        self.Potions = [potion for potion in self.Potions if potion.ID != potion_id]

    def spawn_treasure(self) -> None:
        """
        here we spawn a new treasure with a specifc ID
        :return: None
        """
        self.Treasure = []
        treasure_spawn_points = {
            0: [(6, 4)],
            1: [],
            2: [],
            3: [],
            4: [(6, 6)]
        }
        if self.current_room_index in treasure_spawn_points:
            if self.current_room_index not in self.treasure_states:
                self.treasure_states[self.current_room_index] = [True] * len(
                    treasure_spawn_points[self.current_room_index])
            for i, (x, y) in enumerate(treasure_spawn_points[self.current_room_index]):
                if self.treasure_states[self.current_room_index][i]:
                    self.Treasure.append(
                        Treasure(1 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))

    def check_collision_with_treasure(self) -> None:
        """
        collision detection method: 2 ways: mouse and Pos.X,Pos.Y
        :return: None
        """
        for treasure in self.Treasure:
            if self.PlayerM.Pos.intersects_With(treasure.Pos):
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
                    if (treasure.Pos.Location.X <= mouse_x <= treasure.Pos.Location.X + treasure.Pos.Size.X and
                            treasure.Pos.Location.Y <= mouse_y <= treasure.Pos.Location.Y + treasure.Pos.Size.Y):
                        self.interacting_treasure = treasure
                        treasure.hit_player(self.PlayerM.Pos)
                        break

    def handle_treasure_interaction(self):
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        if 45 < mouse_x < 84 and 55 < mouse_y < 64:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.interacting_treasure.open()
                self.PlayerM.score += 50
                self.treasure_collected(self.interacting_treasure.ID)
                self.interacting_treasure = None
        if pyxel.btnp(pyxel.KEY_O):
            self.interacting_treasure.open()
            self.PlayerM.score += 50
            self.treasure_collected(self.interacting_treasure.ID)
            self.interacting_treasure = None
        if 45 < mouse_x < 84 and 63 < mouse_y < 68:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.interacting_treasure.interaction = False
                self.interacting_treasure = None
        elif pyxel.btnp(pyxel.KEY_I):
            self.interacting_treasure.interaction = False
            self.interacting_treasure = None

    def treasure_collected(self, treasure_id):
        """
        update the state of the treasure, and according to that we handle their visuals
        :param treasure_id:
        :return: None
        """
        room_index = self.current_room_index
        if room_index in self.treasure_states and treasure_id < len(self.treasure_states[room_index]):
            self.treasure_states[room_index][treasure_id] = False
        # Do not remove the treasure from the list, instead, update its state
        for treasure in self.Treasure:
            if treasure.ID == treasure_id:
                treasure.open()

    def spawn_grass(self) -> None:
        """
        here we spawn a new grass with a specifc ID
        :return: None
        """
        self.Grass = []
        grass_spawn_points = {
            0: [(1, 3), (1, 4), (4, 1), (4, 2), (5, 1), (5, 2), (6, 1), (6, 2)],
            1: [(0, 4), (1, 4), (5, 5), (6, 5), (7, 1)],
            2: [(3, 3), (3, 4), (5, 4), (7, 1), (7, 2)],
            3: [(2, 6), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
                (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                (5, 3), (5, 4), (5, 5), (5, 6),
                (6, 3), (6, 4), (6, 5), (6, 6),
                (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)],
            4: [(6, 5)]
        }
        if self.current_room_index in grass_spawn_points:
            for (x, y) in grass_spawn_points[self.current_room_index]:
                self.Grass.append(Grass(5 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))

        def grass_collected(self, grass_id) -> None:
            raise NotImplementedError

        def hit_grass(self) -> None:
            raise NotImplementedError

    def spawn_boxes(self) -> None:
        """
        here we spawn a new box with a specifc ID
        :return: None
        """
        self.Boxes = []
        box_spawn_points = {
            0: [(2, 1), (3, 6), (4, 5), (5, 5)],
            1: [],
            2: [(2, 4), (4, 4), (6, 4), (3, 5), (4, 5)],
            3: [(1, 1), (0, 5), (1, 4)],
            4: []
        }

        if self.current_room_index in box_spawn_points:
            if self.current_room_index not in self.box_positions:
                self.box_positions[self.current_room_index] = box_spawn_points[self.current_room_index]

            for i, (x, y) in enumerate(self.box_positions[self.current_room_index]):
                self.Boxes.append(Box(6 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))

    def save_box_positions(self) -> None:
        self.box_positions[self.current_room_index] = [box.save_position() for box in self.Boxes]

    def load_box_positions(self) -> None:
        if self.current_room_index in self.box_positions:
            saved_positions = self.box_positions[self.current_room_index]
            for i, pos in enumerate(saved_positions):
                if i < len(self.Boxes):
                    self.Boxes[i].load_position(pos)

    def spawn_enemies(self) -> None:
        """
        here we spawn a new enemy with a specifc ID
        :return: None
        """
        self.Enemies = []
        enemy_spawn_points = {
            0: [(3, 2)],
            1: [(5, 2.5)],
            2: [(0, 5), (6, 5)],
            3: [],
            4: [(2, 2), (5, 2), (3.5, 5)]
        }
        if self.current_room_index in enemy_spawn_points:
            if self.current_room_index not in self.enemy_positions:
                self.enemy_positions[self.current_room_index] = enemy_spawn_points[self.current_room_index]

            for i, (x, y) in enumerate(self.enemy_positions[self.current_room_index]):
                self.Enemies.append(Enemy(2 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))
                # self.Enemies[i].draw_hp_bar()

    def save_enemy_positions(self) -> None:
        self.enemy_positions[self.current_room_index] = [enemy.save_position() for enemy in self.Enemies]

    def load_enemy_positions(self) -> None:
        if self.current_room_index in self.enemy_positions:
            saved_positions = self.enemy_positions[self.current_room_index]
            for i, pos in enumerate(saved_positions):
                if i < len(self.Enemies):
                    self.Enemies[i].load_position(pos)

    def update_enemies(self) -> None:
        for enemy in self.Enemies:
            enemy.update()

    def check_enemy_hits(self, attack_rect: Rect, how_much_dmg: int) -> None:
        """
        We use this function in player.attack() and in player.fire_gun() to see when he hits an enemy
        :param attack_rect: Rect
        :return: None
        """
        for enemy in self.Enemies:
            if attack_rect.intersects_With(enemy.Pos):
                if how_much_dmg == 1:
                    enemy.take_damage(50)
                if how_much_dmg == 2:
                    enemy.take_damage(30)
                if how_much_dmg == 3:
                    enemy.take_damage(2)
                if enemy.is_dead:
                    self.PlayerM.score += 5
                    #  print(f"Enemy {enemy.ID} is dead")

    def enemy_died(self, enemy_id: int) -> None:
        """
        we handle here the enemies wif they die, later we can add a life bar for each enemy and delete it - enemy.is_dead
        :param enemy_id:
        :return: None
        """
        room_index = self.current_room_index
        if room_index in self.enemy_states and enemy_id < len(self.enemy_states[room_index]):
            self.enemy_states[room_index][enemy_id] = False

        self.Enemies = [enemy for enemy in self.Enemies if not enemy.is_dead]


def main() -> None:
    App()


if __name__ == '__main__':
    main()

"""
Player.py

if world = 1:
    do this physik
if world = 2:
    do this physik

handle more enemies    

the walls are in Sprite, maybe we need to change that later
"""



