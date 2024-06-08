from sprite import Sprite, Rect
import pyxel


MAP_WITDH = 8
MAP_LENGTH = 8
TILE_SIZE = 16


class Enemy( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Enemy, self).__init__( idx, pos, img, app)
        self.hp = 50  

    def draw( self ):
        super( Enemy, self ).draw()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.app.Enemy.remove(self)