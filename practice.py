from practice_support import *

class Tile(object):
    """An abstract class from which all instantiable types of tiles inheret. Provides the default tile behaviour, which
    can be inhereted or overwritten by specific types of tiles. The __init__ methods for all tiles do not take any
    arguments beyond self.
    """
    
    _type = 'Abstract Tile'
    
    def is_blocking(self) -> bool:
        """Returns True only when this tile is blocking. A tile is blocking if an entity would not be able to move onto that
        tile. By default, tiles are non-blocking."""
        return False
    
    def get_type(self) -> str:
        """Returns a string representing the type of this tile. For the abstract Tile class, this method returns the string
        ‘Abstract Tile’. For instantiable subclasses, this method should return the single letter constant corresponding
        to that class."""
        return self._type
    
    def __str__(self) -> str:
        """Returns a string representing the type of this tile. In most cases, this will be the same string as would be
        returned by get_type."""
        return self.get_type()
    
    def __repr__(self) -> str:
        """Operates identically to the __str__ method."""
        return str(self)  # return self.__str__()
        

class Floor(Tile):
    """Floor is a basic type of tile that represents an empty space on which entities can freely move. It is non-blocking
    and is represented by a single space character."""
    _type = FLOOR
    
    
class Wall(Tile):
    """Wall is a type of tile that represents a wall through which entities cannot pass. Wall tiles are blocking, and are
    represented by the character ‘W’.
    """
    _type = WALL    
    
    def is_blocking(self) -> bool:
        """Walls are blocking."""
        return True
    

class Goal(Tile):
    """Goal is a type of tile that represents a goal location for a crate. Goal tiles are non-blocking, and the type
    is represented by ‘G’. Goal tiles can either be filled (e.g. contain a crate) or unfilled (e.g. empty, with room
    for one crate). Goal tiles start unfilled, and become filled throughout gameplay as the player pushes crates
    onto them. If a goal tile is unfilled, the __str__ and __repr__ methods return ‘G’. However, when a goal tile
    becomes filled, the __str__ and __repr__ methods should instead return ‘X’ to denote that this goal tile is
    filled. """
    _type = GOAL
    
    def __init__(self) -> None:
        super().__init__()
        self._fill = False
    
    def is_filled(self) -> bool:
        """Returns True only when the goal is filled."""
        return self._fill
        
    def fill(self):
        """Sets this goal to be filled."""
        self._fill = True
        self._type = FILLED_GOAL
    

class Entity(object):
    """Abstract base class from which all entities inherit. The __init__ methods for this class does not take any
    arguments beyond self."""
    _type = 'Abstract Entity'
    
    def get_type(self) -> str:
        """Returns a string representing the type of this entity. For the abstract Entity class, this method returns
        the string ‘Abstract Entity’. For instantiable subclasses, this method should return the single letter constant
        corresponding to that class."""
        return self._type

    def is_moveable(self) -> bool:
        """Returns True iff this entity is movable. By default, entities are not movable."""
        return False
    
    def __str__(self) -> str:
        """Returns a string representing the type of this entity. In most cases, this will be the same string as would be
        returned by get_type."""
        return self.get_type()
    
    def __repr__(self) -> str:
        """Operates identically to the __str__ method."""
        return str(self)


class Crate(Entity):
    """Crate is a movable entity, represented (in get_type) by the letter ‘C’. Crates are constructed with a strength
    value, which represents the strength a player is required to have in order to move that crate. The string 
    representation of a crate should be the string version of its strength value."""
    _type = CRATE
    
    def __init__(self, strength: int) -> None:
        """Ensure any code from the Entity constructor is run, and set this crate’s strength value to strength."""
        super().__init__()
        self._strength = strength
        
    def get_strength(self) -> int:
        """Returns this crate’s strength value."""
        return self._strength

    def __str__(self) -> str:
        return str(self.get_strength())
    
    def __repr__(self) -> str:
        return str(self)
    

class Potion(Entity):
    """This is an abstract class which provides a simple interface which all instances of potions must implement. The
    __init__ method for all potions do not take any arguments besides self. Since this class inherits from Entity,
    it (along with its subclasses) should also provide all methods available from the Entity class. Potions are not
    movable. An abstract potion is represented by ‘Potion’ and has no effect."""
    _type = 'Potion'
    
    def effect(self) -> dict[str, int]:
        """Returns a dictionary describing the effect this potion would have on a player. Note that potions are not
        responsible for applying their effects to a player; they only need to provide information about the effects they
        would cause. The abstract potion class should just return an empty dictionary, since it has no effect."""
        return dict()
    

class StrengthPotion(Potion):
    """A StrengthPotion is represented by the string ‘S’ and provides the player with an additional 2 strength."""
    _type = STRENGTH_POTION
    
    def effect(self) -> dict[str, int]:
        """The strength potion class should return a dictionary with strength: 2"""
        return {'strength': 2}
    
class MovePotion(Potion):
    """A MovePotion is represented by the string ‘M’ and provides the player with 5 more moves."""
    _type = MOVE_POTION
    
    def effect(self) -> dict[str, int]:
        """The move potion class should return a dictionary with moves: 5"""
        return {'moves': 5}

    
class FancyPotion(Potion):
    """A FancyPotion is represented by the string ‘F’ and provides the player with an additional 2 strength and 2
    more moves."""
    _type = FANCY_POTION
    
    def effect(self) -> dict[str, int]:
        """The fancy potion class should return a dictionary with moves: 2 and strength: 2"""
        return {'strength': 2,'moves': 2}


class Player(Entity):
    """Player is a movable entity, represented by the letter ‘P’. A player instance is constructed with a starting
    strength and an initial number of moves remaining. These two values can change throughout regular gameplay,
    or through the use of potions, via methods provided by the Player class. A player is only movable if they have
    a positive number of moves remaining."""
    _type = PLAYER
    
    def __init__(self, start_strength: int, moves_remaining: int) -> None:
        """Ensure any code from the Entity constructor is run, and set this player’s strength to start_strength and
        their remaining moves to moves_remaining."""
        super().__init__()
        self._start_strength = start_strength
        self._moves_remaining = moves_remaining
        
    def is_moveable(self) -> bool:
        return True
        
    def get_strength(self) -> int:
        """Returns the player’s current strength value."""
        return self._start_strength
    
    def get_moves_remaining(self) -> int:
        """Returns the player’s current number of moves remaining."""
        return self._moves_remaining
    
    def add_strength(self, amount: int) -> None:
        """Adds the given amount to the player’s strength value."""
        self._start_strength += amount
        
    def add_moves_remaining(self, amount: int) -> None:
        """Adds the given amount to the player’s number of remaining moves. Note that amount may be negative."""
        self._moves_remaining += amount
        
    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        """Applies the effects described in potion_effect to this player."""
        self.add_strength(potion_effect.get("strength", 0))
        self.add_moves_remaining(potion_effect.get("moves", 0))
    

def convert_maze(game: list[list[str]]) -> tuple[Grid, Entities, Position]:
    """This function converts the simple format of the maze representation into a more sophisticated representation."""
    grid: Grid = list()
    entities: Entities = dict()
    player_position: Position = None
    for i in range(len(game)):
        row = game[i]
        temp = list()
        for j in range(len(row)):
            # (i, j) -> Tile | Entity | Player
            position = i, j
            char: str = row[j]  # W, 1, G, P
            if char == WALL:
                temp.append(Wall())
            elif char == GOAL:
                temp.append(Goal())
            elif char == FILLED_GOAL:
                goal = Goal()
                goal.fill()
                temp.append(goal)
            elif char == FLOOR:
                temp.append(Floor())
            elif char.isdigit():
                strength = int(char)
                crate = Crate(strength=strength)
                entities[position] = crate
            elif char == STRENGTH_POTION:
                entities[position] = StrengthPotion()
            elif char == MOVE_POTION:
                entities[position] = MovePotion()
            elif char == FANCY_POTION:
                entities[position] = FancyPotion()
            elif char == PLAYER:
                player_position = position
        grid.append(temp)
    return grid, entities, player_position


class SokobanModel(object):
    """"""
    def __init__(self, maze_file: str) -> None:
        """This method should read the given maze file, call the convert_maze function to get
        representations for the maze, non-player entities, and player position, and construct 
        a player instance with the player stats described in the maze file.
        
        Parameters:
            maze_file(str): filename of the maze to load
        """
        raw_maze, player_stats = read_file(maze_file)
        self._grid, self._entities, self._player_position = convert_maze(raw_maze)
        player_strength, moves = player_stats
        self._player = Player(player_strength, moves)
        self._rows = len(self._grid)        
        self._cols = len(self._grid[0])
        

    def get_maze(self) -> Grid:
        """Returns the maze representation (list of lists of Tile instances)."""
        return self._grid
    
    def get_entities(self) -> Entities:
        """Returns the dicitonary mapping positions to non-player entities."""
        return self._entities
    
    def get_player_position(self) -> Position:
        """Returns the player’s current position."""
        return self._player_position
    
    def get_player_moves_remaining(self) -> int:
        """Returns the number of moves the player has remaining."""
        return self._player.get_moves_remaining()
    
    def get_player_strength(self) -> int:
        """Returns the player’s current strength."""
        return self._player.get_strength()
    
    def attempt_move(self, direction: str) -> bool:
        """"""
        # check if direction is valid
        if direction not in DIRECTION_DELTAS:
            return False
        dx, dy = DIRECTION_DELTAS[direction]
        x1, y1 = self.get_player_position()
        x2, y2 = x1 + dx, y1 + dy
        # check if new position would be out of bounds
        if x2 < 0 or x2 >= self._rows:
            return False
        if y2 < 0 or y2 >= self._cols:
            return False
        # check if blocked by a blocking tile
        tile: Tile = self._grid[x2][y2]
        if tile.is_blocking():
            return False
        # see if it's a crate
        entity = self._entities.get((x2, y2))
        if isinstance(entity, Crate):
            # not enough strength
            if self.get_player_strength() < entity.get_strength():
                return False
            x3, y3 = x2 + dx, y2 + dy

            # check if new position would be out of bounds
            if x3 < 0 or x3 >= self._rows:
                return False
            if y3 < 0 or y3 >= self._cols:
                return False
            # check if blocked by a blocking tile
            tile: Tile = self._grid[x3][y3]
            if tile.is_blocking():
                return False
            if self._entities.get((x3, y3)):
                return False
            if isinstance(tile, Goal):
                if not tile.is_filled():
                    # remove the crate
                    self._entities.pop((x2, y2))
                    # set goal to be filled
                    tile.fill()
                    # move player to crate's position
                    self._player_position = (x2, y2)
                    # update moves
                    self._player.add_moves_remaining(-1)
                    return True
            # move the crate to new position (x3, y3)
            self._entities[(x3, y3)] = entity
            self._entities.pop((x2, y2))
            self._player_position = (x2, y2)
            self._player.add_moves_remaining(-1)
            return True
            
        elif isinstance(entity, Potion):
            self._entities.pop((x2, y2))
            self._player.apply_effect(entity.effect())
            # move player to crate's position
            self._player_position = (x2, y2)
            # update moves
            self._player.add_moves_remaining(-1)
            return True
        else:
            # move player to crate's position
            self._player_position = (x2, y2)
            # update moves
            self._player.add_moves_remaining(-1)
            return True
    
    def has_won(self) -> bool:
        """Returns True only when the game has been won. The game has been won if all goals are filled, or equivalently
        (since the number of goals is always equal to the number of crates), there are no more crates on the grid."""
        for row in self._grid:
            for tile in row:
                if isinstance(tile, Goal):
                    if not tile.is_filled():
                        return False
        return True
    
    
class Sokoban(object):
    """The Sokoban class represents the controller class in the MVC structure. It is responsible for instantiating the
    model class (that you just wrote) and the view class (which is provided in a2_support.py). The controller class
    handles events (such as user input) and facilitates communication between the model and view classes. The
    Sokoban class must implement the following methods."""
    def __init__(self, maze_file: str) -> None:
        """This method should construct an instance of the SokobanModel class using the provided maze_file, as well as
        an instance of the SokobanView class."""
        self._model = SokobanModel(maze_file=maze_file)
        self._view = SokobanView()
    
    def display(self) -> None:
        """This method should call the display_game and display_stats methods on the instance of the SokobanView
        class. The arguments given should be based on the state of the game as defined by the SokobanModel
        instance."""
        self._view.display_game(
            maze=self._model.get_maze(),
            entities=self._model.get_entities(),
            player_position=self._model.get_player_position()
        )
        self._view.display_stats(
            moves_remaining=self._model.get_player_moves_remaining(),
            strength=self._model.get_player_strength()
        )
        
    def play_game(self) -> None:
        """"""
        while not self._model.has_won():
            self.display()
            command = input("Enter move: ")
            if command.lower() == 'q':
                return
            is_moved = self._model.attempt_move(command)
            if not is_moved:
                print("Invalid move\n")
                continue
            if self._model.get_player_moves_remaining() == 0:
                print("You lost!")
                return
        print("You won!")
        
    
def main():
    game = Sokoban(maze_file="maze_files/maze1.txt")
    game.play_game()
    
    
    
    
if __name__ == "__main__":
    main()