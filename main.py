"""Lumina"""
"""i love u too"""
"""Project started in 2024 by Esriges Ri and Bogigis Dar <3"""

import pyxel
from player import Player
from enemy import Enemy
from items import Potion, Treasure, Grass, Box
from sprite import Rect

MAP_WIDTH = 8
MAP_LENGTH = 8
TILE_SIZE = 16

class App:
    def __init__(self):
        pyxel.init(TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_LENGTH + 8, title="Lumina", display_scale=6, fps=60)
        pyxel.load("main.py.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.mouse(True)

        self.menu = True
        self.new_room = True
        self.room_coordinates = [(0, 0), (16, 0), (32, 0), (48, 0), (64, 0)]
        self.current_room_index = 0
        self.aim_direction = "R"
        self.visited_P = set()  #no need for now but here i am handling the items, enemies spawns in a room
        self.enemy_states = {}  
        self.potion_states = {}
        self.treasure_states = {}
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

        self.start()
        self.initialize_entities()
        pyxel.run(self.update, self.draw)

    def start(self):
        self.size_obj = 1
        self.PlayerM = Player(0, Rect(1 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE * self.size_obj, TILE_SIZE * self.size_obj), 0, self, Rect(20, 23, 5, 5))

    def initialize_entities(self):
        self.Enemies = []
        self.Boxes = []
        self.Grass = []
        self.Treasure = []
        self.Potions = []
        self.spawn_entities()

    def update(self):
        if self.GameOver:
            self.menu = True
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_RETURN):
            self.menu = False

        if self.game_Start:
            self.PlayerM.key()
            self.room_change()
            self.PlayerM.check_collision_with_enemies()
            self.PlayerM.check_collision_with_potion()
            self.PlayerM.check_collision_with_treasure()

    def draw(self):
        if self.menu:
            self.GameOver = False
            self.game_Start = False
            self.new_room = True
            self.current_room_index = 0 
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 128 * 2, 128, 128)
            pyxel.text(16 * 1.5, 16 * 4, "Press ENTER to play", 6)
        else:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, self.room_coordinates[self.current_room_index][0] * 8, self.room_coordinates[self.current_room_index][1] * 8, pyxel.width, pyxel.height)
            self.game_Start = True
            if self.new_room:
                self.spawn_entities()
            for entity_list in [self.Enemies, self.Grass, self.Potions, self.Treasure, self.Boxes]:
                for entity in entity_list:
                    entity.draw()
            self.PlayerM.draw()

    def room_change(self):
        player_x = self.PlayerM.Pos.Location.X
        player_y = self.PlayerM.Pos.Location.Y
        self.new_room = False

        if player_x >= pyxel.width - 1:
            self.current_room_index = min(self.current_room_index + 1, len(self.room_coordinates) - 1)
            self.PlayerM.Pos.Location.X = 0
            self.new_room = True

        elif player_x < -11 and player_y <= 32:
            self.current_room_index = max(self.current_room_index - 1, 0)
            self.PlayerM.Pos.Location.X = pyxel.width - TILE_SIZE
            self.new_room = True

        if self.new_room:
            self.spawn_entities()

    def spawn_entities(self):
        for spawn_method in self.entity_spawners.values():
            spawn_method()

    def spawn_potion(self):
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
                    self.Potions.append(Potion(4 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))

    def potion_collected(self, potion_id):
        room_index = self.current_room_index
        if room_index in self.potion_states and potion_id < len(self.potion_states[room_index]):
            self.potion_states[room_index][potion_id] = False

        self.Potions = [potion for potion in self.Potions if potion.ID != potion_id]


    def spawn_treasure(self):
        self.Treasure = []
        treasure_spawn_points = {
            0: [(6, 4), (1,6)],
            1: [],
            2: [],
            3: [],
            4: [(6, 6)]
        }
        if self.current_room_index in treasure_spawn_points:
            if self.current_room_index not in self.treasure_states:
                self.treasure_states[self.current_room_index] = [True] * len(treasure_spawn_points[self.current_room_index])
            for i, (x, y) in enumerate(treasure_spawn_points[self.current_room_index]):
                if self.treasure_states[self.current_room_index][i]:
                    self.Treasure.append(Treasure(1 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))

    def check_collision_with_treasure(self):
        for treasure in self.Treasure:
            if self.PlayerM.Pos.intersects_With(treasure.Pos):
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
                    if (treasure.Pos.Location.X <= mouse_x <= treasure.Pos.Location.X + treasure.Pos.Size.X and
                        treasure.Pos.Location.Y <= mouse_y <= treasure.Pos.Location.Y + treasure.Pos.Size.Y):
                        self.PlayerM.score += 50
                        self.treasure_collected(treasure.ID)
                        break  

    def treasure_collected(self, treasure_id):
        room_index = self.current_room_index
        if room_index in self.treasure_states and treasure_id < len(self.treasure_states[room_index]):
            self.treasure_states[room_index][treasure_id] = False
        self.Treasure = [treasure for treasure in self.Treasure if treasure.ID != treasure_id]


    def spawn_grass(self):
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

    def spawn_boxes(self):
        self.Boxes = []
        box_spawn_points = {
            0: [(2, 1), (3, 6), (4, 5), (5, 5)],
            1: [],
            2: [(2, 4), (4, 4), (6, 4), (3, 5), (4, 5)],
            3: [(0, 1), (0, 2), (0, 5), (1, 4)],
            4: []
        }
        if self.current_room_index in box_spawn_points:
            for (x, y) in box_spawn_points[self.current_room_index]:
                self.Boxes.append(Box(6 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))

    def spawn_enemies(self):
        self.Enemies = []
        enemy_spawn_points = {
            0: [(3, 1)],
            1: [(5, 2.5)],
            2: [(0, 5), (6, 5)],
            3: [],
            4: [(2, 2), (5, 2), (3.5, 5)]
        }
        if self.current_room_index in enemy_spawn_points:
            if self.current_room_index not in self.enemy_states:
                self.enemy_states[self.current_room_index] = [True] * len(enemy_spawn_points[self.current_room_index])
            for i, (x, y) in enumerate(enemy_spawn_points[self.current_room_index]):
                if self.enemy_states[self.current_room_index][i]:
                    self.Enemies.append(Enemy(2 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, i, self))
    
    def check_enemy_hits(self, attack_rect):
        for enemy in self.Enemies:
            if attack_rect.intersects_With(enemy.Pos):
                enemy.take_damage(1)
                if enemy.is_dead:
                    self.PlayerM.score += 5
                    print(f"Enemy {enemy.ID} is dead")

    def enemy_died(self, enemy_id):
        room_index = self.current_room_index
        if room_index in self.enemy_states and enemy_id < len(self.enemy_states[room_index]):
            self.enemy_states[room_index][enemy_id] = False

        self.Enemies = [enemy for enemy in self.Enemies if not enemy.is_dead]




App()




"""
Player.py

if world = 1:
    do this physik
if world = 2:
    do this physik

handle more enemies    

the walls are in Sprite, maybe we need to change that later
"""