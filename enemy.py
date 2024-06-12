from sprite import Sprite, Rect
import pyxel


MAP_WITDH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Enemy( Sprite ):
    def __init__( self, idx, pos, img, id, app ):
        super( Enemy, self).__init__( idx, pos, img, app)
        self.ID = id
        self.hp = 50  
        self.is_dead = False  


    def draw( self ):
        super( Enemy, self ).draw(0)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.app.Enemies.remove(self)
            self.is_dead = True  
            self.app.enemy_died(self.ID) 