import random
import logging
import enum

LOGGER = logging.getLogger(__name__)

class Direction(enum.Enum):
    """Stellt die Bewegungsrichtungen dar"""
    UP = (0,-1)
    RIGHT = (1,0)
    DOWN = (0,1)
    LEFT = (-1,0)

    def __init__(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y

    @classmethod
    def parse(cls, text):
        return Direction[text.upper()]

class GameState():    
    WIDTH = 4
    HEIGHT = 4

    def __init__(self):
        # Erstelle das leere 2D-Array
        self.game_grid = [[None for y in range(self.HEIGHT)] for x in range(self.WIDTH)]
        
        # Füge 2 Zahlen ein
        self.spawn_nr(amount=2)

    def handle_key(self, dir):
        dir = Direction.parse(dir)
        LOGGER.info('moving in direction: {}'.format(dir))
        moved_any = False
        dir_x, dir_y = dir.dir_x, dir.dir_y
        x_iter = range(0, self.WIDTH, 1) if dir_x < 0 else range(self.WIDTH-1, -1, -1)
        y_iter = range(0, self.HEIGHT, 1) if dir_y < 0 else range(self.WIDTH-1, -1, -1)
        for x in x_iter:
            for y in y_iter:
                nr = self.game_grid[x][y]
                if nr is not None:
                    moved = self.move_in_dir(x, y, dir)
                    LOGGER.info('({},{}) moved: {}'.format(x,y, moved))
                    moved_any = moved_any or moved 
        if moved_any:
            self.spawn_nr()
        return len(set(self.free_fields())) == 0

    def move_in_dir(self, x, y, dir):
        """
        Bewegt Zahl so weit wie möglich in Richtung. Gibt True zurück,
        wenn eine Bewegung stattfand
        """
        nr = self.game_grid[x][y]
        if nr is not None:
            # Postion zu der sich Nummer bewegt
            target_x, target_y = self.get_target_pos(nr, x, y, dir)
            LOGGER.info('moving {} from {},{} to {},{}'.format(nr, x, y, target_x, target_y))
            # lösche alte Nummer
            self.game_grid[x][y] = None

            # Schreibe Nummer an neue Postion
            target_nr = self.game_grid[target_x][target_y]
            self.game_grid[target_x][target_y] = 2 * nr if target_nr is not None else nr
            return target_x != x or target_y != y
        return False


    def get_target_pos(self, nr, x, y, dir):
        """Berechne die Postion in die sich die Nummer bewegen kann"""

        # Addire dir_x und dir_y um 1 Schritt in Richtung zu gehen
        dir_x, dir_y = dir.dir_x, dir.dir_y
        
        # Position die als nächstes überprüft wird
        next_x = x + dir_x
        next_y = y + dir_y
        
        # Solange nächste Postion noch im Feld ist
        while next_x >= 0 and next_x < GameState.WIDTH and next_y >= 0 and next_y < GameState.HEIGHT:
            if self.game_grid[next_x][next_y] is not None:
                # wenn bei nächster Position gleiche nr ist vereinige
                if nr == self.game_grid[next_x][next_y]:
                    return next_x, next_y
                # wenn andere nummer gehe zur letzten postion
                else:
                    return x, y
            # wenn leer überprüfe nächstes Feld
            x, y = next_x, next_y
            next_x += dir_x 
            next_y += dir_y
        return x, y

    def spawn_nr(self, amount=1):
        spawns = random.sample(set(self.free_fields()), amount)
        LOGGER.info('spawning nrs at: {}'.format(spawns))
        for x, y in spawns:
            self.game_grid[x][y] = 2

    def free_fields(self):
        for x, y in self.all_positions():
            if self.game_grid[x][y] is None:
                yield (x,y)

    def all_positions(self):
        for x, row in enumerate(self.game_grid):
            for y, _ in enumerate(row):
                yield (x,y) 

    

    

    
