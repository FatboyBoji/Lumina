from sprite import Sprite


MAP_WITDH = 8
MAP_LENGTH = 8
TILE_SIZE = 16




class Potion(Sprite):
    def __init__(self, idx, pos, img, potion_id, app):
        super(Potion, self).__init__(idx, pos, img, app)
        self.ID = potion_id
        self.collected = False  

    def draw(self):
        super(Potion, self).draw(0)


class Treasure(Sprite):
    def __init__(self, idx, pos, img, treasure_id, app):
        super(Treasure, self).__init__(idx, pos, img, app)
        self.ID = treasure_id
        self.collected = False  

    def draw(self):
        super(Treasure, self).draw(0)


class Grass( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Grass, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( Grass, self ).draw(0)


class Box( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Box, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( Box, self ).draw(0)      

"""
sprite:
    maybe we changge sprite, because it has to many attributes of player and other classes.

portal:
    want to add the entity portal. 
    should have different atributes, 

world

movement of enemy

Bugfixes:
    shots fired - new.room = True
    walk collision should be fixed or changed

"""