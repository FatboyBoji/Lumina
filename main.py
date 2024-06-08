"""Lumina"""
"""i love u too"""
"""Project started in 2024 by Esriges Ri and Bogigis Dar <3"""


import pyxel
from player import Player
from enemy import Enemy
from items import Potion, treasure, Grass, Box
from sprite import Rect


MAP_WITDH = 8
MAP_LENGTH = 8


class App:
    def __init__( self ):
        global TILE_SIZE
        TILE_SIZE = 16
        pyxel.init(TILE_SIZE * MAP_WITDH, TILE_SIZE * MAP_LENGTH + 8, title="Lumina", display_scale=6, fps=60)  #extra space for hp, score,etc  , display_scale=6
        pyxel.load("main.py.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.mouse(True)

        self.start()
        self.menu = True
        self.new_room = True
        self.room_coordinates = [(0, 0), (16, 0), (32, 0), (48, 0), (64, 0)]    #(16, 0)
        self.current_room_index = 0
        self.i = 0
        self.aim_direction = "R"
        self.map_x = 0
        self.map_y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.Enemy = []  
        self.spawn_enemies() 
        self.Boxes = []
        self.spawn_boxes()
        self.grass = []
        self.spawn_grass()
        self.treasure = []
        self.spawn_treasure()
        self.potion = []
        self.visited_P = 0
        self.spawn_potion()
        self.GameOver = False
        self.hp_bar = 6

        pyxel.run(self.update, self.draw)

    def start(self):
        self.size_obj = 1
        self.PlayerM = Player( 0, Rect(1 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE*self.size_obj, TILE_SIZE*self.size_obj), 0, self, Rect(16,16,12,12)) #could add bigger size objects in here with objt_size


    def update(self):
        if self.GameOver:
            self.menu = True
        if pyxel.btnp(pyxel.KEY_Q):                 #this should be ignored in the code, not part of the game
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_RETURN):
            self.menu = False

        self.PlayerM.key()
        self.room_change()
        self.PlayerM.check_collision_with_enemies()
        self.PlayerM.check_collision_with_potion()

    def draw(self):
        if self.menu:
            self.GameOver = False
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 128*2, 128, 128)
            pyxel.text(16 * 1.5, 16 * 4, "Press ENTER to play", 6)
        else:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, self.room_coordinates[self.current_room_index][0]*8, self.room_coordinates[self.current_room_index][1]*8, pyxel.width, pyxel.height)
            #pyxel.text(16 * 4, 16 * 8+2, "score: ", 6)
            for e in self.Enemy:
                e.draw()     
            for g in self.grass:
                g.draw()  
            for p in self.potion:
                p.draw()
            for t in self.treasure:
                t.draw() 
            for b in self.Boxes:
                b.draw()            
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
        self.spawn_enemies()
        self.spawn_boxes()
        self.spawn_grass()
        self.spawn_treasure()
        self.spawn_potion()



    def spawn_potion( self ):
        self.potion = [] 
        potion_spawn_points = {
            0: [ (3,5) ],
            1: [],
            2: [ (6,6) ],
            3: [], 
            4: []
        }
        if self.current_room_index in potion_spawn_points and self.visited_P == self.current_room_index:
            #self.visited_P =+ 1    # the goal is: if the potion is consumed, it should not apear again after reentering the same room
            for (x, y) in potion_spawn_points[self.current_room_index]:
                self.potion.append(Potion(4 * 32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))

    def check_potion_heal(self):
        for enemy in self.Enemy:
            if self.PlayerM.Pos.intersects_With(enemy.Pos):
                self.PlayerM.heal(2)


    def spawn_treasure( self ):
        self.treasure = []
        treasure_spawn_points = {
            0: [ (6,4) ],
            1: [],
            2: [],
            3: [],
            4: [ (6,6) ]
        }
        if self.current_room_index in treasure_spawn_points:
            for (x, y) in treasure_spawn_points[self.current_room_index]:
                self.treasure.append(treasure(1*32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))


    def spawn_grass( self ):
        self.grass = []
        grass_spawn_pionts = {
            0: [ (1,3), (1,4), (4,1), (4,2), (5,1), (5,2), (6,1), (6,2) ],    
            1: [ (0,4), (1,4), (5,5), (6,5), (7,1) ],
            2: [ (3,3), (3,4), (5,4), (7,1), (7,2) ],
            3: [ (2,6), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6),
                 (4,1), (4,2), (4,3), (4,4), (4,5), (4,6),
                 (5,3), (5,4), (5,5), (5,6),
                 (6,3), (6,4), (6,5), (6,6),
                 (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), ],
            4: [ (6,5) ]
        }
        if self.current_room_index in grass_spawn_pionts:
            for (x, y) in grass_spawn_pionts[self.current_room_index]:
                self.grass.append(Grass(5*32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))



    def spawn_boxes( self ):
        self.Boxes = []
        box_spawn_points = {
            0: [ (2,1), (3,6), (4,5), (5,5) ],
            1: [],
            2: [ (2,4), (4,4), (6,4), (3,5), (4,5) ],
            3: [ (0,1), (0,2), (0,5), (1,4) ],
            4: []
        }

        if self.current_room_index in box_spawn_points:
            for (x, y) in box_spawn_points[self.current_room_index]:
                self.Boxes.append(Box(6*32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))


    def spawn_enemies(self):
        self.Enemy = []  
        enemy_spawn_points = {
            0: [(3, 1)],
            1: [(5, 2.5)],
            2: [(0, 5), (6, 5)],
            3: [],
            4: [(2, 2), (5, 2), (3.5, 5)]
        }

        if self.current_room_index in enemy_spawn_points:
            for (x, y) in enemy_spawn_points[self.current_room_index]:
                self.Enemy.append(Enemy(2*32, Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0, self))

    def check_enemy_hits(self, attack_rect):
        for enemy in self.Enemy:
            if attack_rect.intersects_With(enemy.Pos):
                enemy.take_damage(1)



App()
