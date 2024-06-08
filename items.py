from sprite import Sprite


MAP_WITDH = 8
MAP_LENGTH = 8
TILE_SIZE = 16




class Potion( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Potion, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( Potion, self ).draw()


class treasure( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( treasure, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( treasure, self ).draw()


class Grass( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Grass, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( Grass, self ).draw()


class Box( Sprite ):
    def __init__( self, idx, pos, img, app ):
        super( Box, self).__init__( idx, pos, img, app)

    def draw( self ):
        super( Box, self ).draw()      