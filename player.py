from sprite import Sprite , Rect
import math
import pyxel
import time


MAP_WITDH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Player( Sprite ):
    def __init__( self, idx, pos, img, app, col ):
        super( Player, self).__init__( idx, pos, img, app )
        self.Col = col
        self.score = 0
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

    def draw(self):
        if self.is_moving == False:
            if self.last_dir in ["y-", "y+"]:
                current_frame = 3
            elif self.last_dir in ["x-", "x+"]:
                current_frame = 0
        if self.is_moving == True:
            current_frame = self.walking_frames[self.last_dir][self.current_frame_index]
        super(Player, self).draw(current_frame)  
        pyxel.rect(0,128,128,8,0)        #pyxel.rect(8,129,16*2+8,7,11)
        pyxel.text(16 * 4, 16 * 8 + 2, f"score: {self.score}", 6)
        self.draw_hp_bar()
        self.fire_gun() 
        if self.epee is not None and time.time() - self.last_epee < 0.2:
            pyxel.rect(self.epee.Location.X, self.epee.Location.Y, self.epee.Size.X, self.epee.Size.Y, 8)  
        if self.epee is not None and time.time() - self.last_epee < 0.2:
            self.draw_laser()
            #pyxel.blt(self.epee.Location.X, self.epee.Location.Y,0,32,80,16,16,0)
        #pyxel.rect(self.Col.Location.X+1.5, self.Col.Location.Y+1.5, self.Col.Size.X, self.Col.Size.Y, 12)

    def key(self):
        self.is_moving = False
        current_time = time.time()
        
        if pyxel.btn(pyxel.KEY_W):  # move up
            new_Y = self.Pos.Location.Y - self.DX
            self.last_dir = "y+"
            if not self.check_tile_collision(self.Pos.Location.X, new_Y, "up"):
                self.Pos.Location.Y = new_Y
                self.Col.Location.Y -= self.DX
                self.is_moving = True

        if pyxel.btn(pyxel.KEY_A):  # move left
            new_X = self.Pos.Location.X - self.DX
            self.last_dir = "x-"
            self.look_direction = +1
            if not self.check_tile_collision(new_X, self.Pos.Location.Y, "left"):
                self.Pos.Location.X = new_X
                self.Col.Location.X -= self.DX
                self.is_moving = True

        if pyxel.btn(pyxel.KEY_D):  # move right
            new_X = self.Pos.Location.X + self.DX
            self.last_dir = "x+"
            self.look_direction = -1
            if not self.check_tile_collision(new_X, self.Pos.Location.Y, "right"):
                self.Pos.Location.X = new_X
                self.Col.Location.X += self.DX
                self.is_moving = True

        if pyxel.btn(pyxel.KEY_S):  # move down
            new_Y = self.Pos.Location.Y + self.DX
            self.last_dir = "y-"
            if not self.check_tile_collision(self.Pos.Location.X, new_Y, "down"):
                self.Pos.Location.Y = new_Y
                self.Col.Location.Y += self.DX
                self.is_moving = True
        
        if self.is_moving and current_time - self.last_animation_time >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.walking_frames[self.last_dir])
            self.last_animation_time = current_time

        if pyxel.btn(pyxel.KEY_SPACE):
            self.attack()
        # KEY_2 is already used in fire_shot()
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
        if pyxel.btn(pyxel.KEY_3):
            if self.moving_animation_num == 0:
                self.moving_animation_num = 2
            else:
                self.moving_animation_num = 0

    def get_tile(self, tile_x, tile_y):
        offset_x = self.app.room_coordinates[self.app.current_room_index][0]
        offset_y = self.app.room_coordinates[self.app.current_room_index][1]
        return pyxel.tilemaps[0].pget(tile_x + offset_x, tile_y + offset_y)

    def check_tile_collision(self, new_x, new_y, direction):
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
        
        for treasure in self.app.Treasure:
            if self.Col.intersects_With(treasure.Pos):
                return True
    
        return tile in self.tile_wall or tile2 in self.tile_wall or tile3 in self.tile_wall

    def draw_laser( self ):
        if self.last_dir == "y-" and self.look_direction == 1:  # Down, left
            pyxel.blt( self.Pos.Location.X - 4, self.Pos.Location.Y + self.Pos.Size.Y - 4,0,32,80,16,16,0 )
        elif self.last_dir == "y-" and self.look_direction != 1:  # Down, right
            pyxel.blt( self.Pos.Location.X + 8, self.Pos.Location.Y + self.Pos.Size.Y - 4,0,32,80,16,16,0 )
        elif self.last_dir == "y+" and self.look_direction == 1 :  # Up, left
            pyxel.blt( self.Pos.Location.X - 4, self.Pos.Location.Y - self.Pos.Size.Y - 4,0,32,80,16,16,0 )
        elif self.last_dir == "y+" and self.look_direction != 1:   # Up, right
            pyxel.blt( self.Pos.Location.X + 8, self.Pos.Location.Y - self.Pos.Size.Y/2 + 2,0,32,80,16,16,0 )
                        

    def draw_hp_bar(self):
        x = 8 
        y = 129  
        heart_width = 8
        img_bank = 0
        for i in range(self.max_health):
            if self.current_health == 0:
                self.app.GameOver = True
                self.Pos.Location.X = 1*TILE_SIZE
                self.Pos.Location.Y = 1*TILE_SIZE
                self.current_health = 10
                self.app.current_room_index = 0
                self.app.new_room = True
            if self.current_health > 10:
                pyxel.blt(x + i * heart_width + 8, y, img_bank, 8, 120, heart_width, heart_width, 0) 
            elif self.current_health > i * 2 + 1:
                #pyxel.blt(x + i * heart_width + 8, y, img_bank, 8, 120, heart_width, heart_width, 0)  # Full heart
                pyxel.blt(x + i * heart_width, y, img_bank, 0, 112, heart_width, heart_width, 0)  # Full heart
            elif self.current_health == i * 2 + 1:
                pyxel.blt(x + i * heart_width, y, img_bank, 8, 112, heart_width, heart_width, 0)  # Half heart
            else:
                pyxel.blt(x + i * heart_width, y, img_bank, 0, 120, heart_width, heart_width, 0)  # Empty heart

    def take_damage(self, amount):
        if self.current_health <= 10:
            self.score -= 5
            self.current_health = max(0, self.current_health - amount)

    def heal(self, amount):
        if self.current_health > 10:
            self.current_health = min( 11, self.current_health + amount)
        if self.current_health <= 10:
            self.current_health = min(self.max_health * 2, self.current_health + amount)

    def check_collision_with_enemies(self):
        current_time = time.time()
        for enemy in self.app.Enemies:
            if self.Pos.intersects_With(enemy.Pos):
                if current_time - self.last_damage_time >= 1:
                    self.take_damage(1)
                    self.last_damage_time = current_time
    
    def check_collision_with_potion(self):
        for potion in self.app.Potions[:]:
            if self.Pos.intersects_With(potion.Pos):
                self.heal(3)
                self.app.potion_collected(potion.ID)

    def check_collision_with_treasure(self):
        self.app.check_collision_with_treasure()

    def move_box(self, direction):
        for box in self.app.Boxes:
            if self.Pos.intersects_With(box.Pos):
                if direction == "left" and self.last_dir == "x-":
                    box_new_X = box.Pos.Location.X - self.DX
                    if not self.check_tile_collision(box_new_X, box.Pos.Location.Y, "left"):
                        box.Pos.Location.X = box_new_X
                        return True  # Indicates box was moved
                elif direction == "right" and self.last_dir == "x+":
                    box_new_X = box.Pos.Location.X + self.DX
                    if not self.check_tile_collision(box_new_X, box.Pos.Location.Y, "right"):
                        box.Pos.Location.X = box_new_X
                        return True
                elif direction == "up" and self.last_dir == "y+":
                    box_new_Y = box.Pos.Location.Y - self.DX
                    if not self.check_tile_collision(box.Pos.Location.X, box_new_Y, "up"):
                        box.Pos.Location.Y = box_new_Y
                        return True
                elif direction == "down" and self.last_dir == "y-":
                    box_new_Y = box.Pos.Location.Y + self.DX
                    if not self.check_tile_collision(box.Pos.Location.X, box_new_Y, "down"):
                        box.Pos.Location.Y = box_new_Y
                        return True
        return False  # Indicates no box was moved


    # Plan for attack(): i want to change it so i can control the directon by the key arrows/ alternative mouse direction c: more dynamic maybe
    def attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            if self.last_dir == "x-":  # Left
                self.epee = Rect(self.Pos.Location.X - self.Pos.Size.X - 8, self.Pos.Location.Y+8, self.Pos.Size.X / 4, self.Pos.Size.Y +8)
            elif self.last_dir == "x+":  # Right
                self.epee = Rect(self.Pos.Location.X + self.Pos.Size.X, self.Pos.Location.Y +8, self.Pos.Size.X / 4, self.Pos.Size.Y + 8)
            elif self.last_dir == "y+" and self.look_direction == 1 :  # Up, left
                self.epee = Rect(self.Pos.Location.X, self.Pos.Location.Y - self.Pos.Size.Y, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            elif self.last_dir == "y+" and self.look_direction != 1:   # Up, right
                self.epee = Rect(self.Pos.Location.X + 12, self.Pos.Location.Y - self.Pos.Size.Y, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            elif self.last_dir == "y-" and self.look_direction == 1:  # Down, left
                self.epee = Rect(self.Pos.Location.X, self.Pos.Location.Y + self.Pos.Size.Y - 4, self.Pos.Size.Y + 8, self.Pos.Size.X / 4) 
            elif self.last_dir == "y-" and self.look_direction != 1:  # Down, right
                self.epee = Rect(self.Pos.Location.X + 12, self.Pos.Location.Y + self.Pos.Size.Y - 4, self.Pos.Size.Y + 8, self.Pos.Size.X / 4)
            self.last_epee = current_time
        self.app.check_enemy_hits(self.epee)

    def fire_gun(self):
        current_time = pyxel.frame_count / 60
        # If the player enters a new room, clear the shot list
        if self.app.new_room:
            self.shot_list = []

        if pyxel.btn(pyxel.KEY_2) and current_time - self.last_shot_time >= self.shot_cooldown:
            self.shot_list.append({"direction": self.last_dir, "x": self.Pos.Location.X + 8, "y": self.Pos.Location.Y + 9})
            self.last_shot_time = current_time 

        for i in range(len(self.shot_list) - 1, -1, -1):
            shot = self.shot_list[i]

            # Draw the shot
            if 0 <= shot["x"] <= pyxel.width and 0 <= shot["y"] <= pyxel.height:
                pyxel.circb(shot["x"], shot["y"], 2, 8)

            if shot["direction"] == "x+":
                shot["x"] += 1
            elif shot["direction"] == "x-":
                shot["x"] -= 1
            elif shot["direction"] == "y+":
                shot["y"] -= 1
            elif shot["direction"] == "y-":
                shot["y"] += 1

            # Check if the shot is out of bounds
            if shot["x"] < 4 or shot["x"] > 124 or shot["y"] < 4 or shot["y"] > 124:
                self.shot_list.pop(i)
                continue

            if self.app.check_enemy_hits( Rect( shot["x"], shot["y"], 4,4)):
                self.shot_list.pop(i)
                continue
