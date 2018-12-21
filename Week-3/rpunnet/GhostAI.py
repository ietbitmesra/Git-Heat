'''
This package controls the ghosts direction for increasing difficulty.
'''

import random

def get_direction(pacman , maze , ghost , AI_level = 0):
    '''
    This function looks at the position of pacman and returns
    a direction toward the pacman with probability according to 
    the AI_level.
    The higher AI_level signifies more probability in the direction of pacman.

    Parameters-
        pacman - Pacman object for pacman's position.
        maze - maze object for locating walls.
        ghost - Ghost object for ghost's position.
        AI_level - Intelligence level of ghost.(0 = completely random choice of direction)
    Returns-
        direction - the chosen direction.
    '''

    directions = []

    # Check for going in the teleporter area
    if round(ghost.y / maze.cell_height) == 13:
        if ghost.x  > (8 * maze.cell_width):
            directions.append('l')
        if ghost.x < ((maze.x_length - 8) * maze.cell_width):
            directions.append('r')
    else:
        directions.extend(['l' , 'r'])

    directions.extend(['d' , 'u'])
    

    direction_pacman_vert = 'u'
    if ghost.y < pacman.y:
        direction_pacman_vert = 'd'

    
    direction_pacman_horiz = 'l'
    if ghost.x < pacman.x:
        direction_pacman_horiz = 'r'

    
    directions_choice = []

    if direction_pacman_horiz in directions:
        directions_choice.extend([direction_pacman_horiz] * AI_level)

    if direction_pacman_vert in directions:
        directions_choice.extend([direction_pacman_vert] * AI_level)

    for direction in directions:
        directions_choice.append(direction)

    return random.choice(directions_choice)
    