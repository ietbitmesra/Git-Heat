''' 
The driver file of the program.
This is where the game is run and controlled.
'''

import pygame   # The library for graphics.

import Maze     # Contains information about the Maze.

import Pacman   # For holding informations about pacman.

import Ghost    # For holding information about each ghost.

import os       # For os.path.join and os.getcwd 

pygame.init()   # Initialising pygame

# Constants.
FPS = 144
WINDOW_HEIGHT = 730
WINDOW_WIDTH = 1000
CAPTION = "PACMAN"
LEVEL = 1
GHOST_RELEASE_DELAY = 2000
CELL_WIDTH = 24
CELL_HEIGHT = 24
BLACK = (0 , 0 , 0)



# Function Definitions - 

def check_win(maze):
    ''' 
    Check if there is any pellet left in the maze.
    Parameters -
        maze - Maze object which contains maze information
    '''
    for row in maze.matrix:
        for cell in row:
            if "pellet" in cell:
                return False
    
    return True



def release_ghost_in_maze(ghosts_in_maze , ghosts_not_in_maze , game_start_time):
    '''
    Releases ghosts in the maze after every 5 seconds.
    It transfers ghosts not in maze to ghost in maze and changes its in_maze value to True.

    Parameters-
        ghost_in_maze - list of ghosts that are in maze.
        ghost_not_in_maze - list of ghosts that are in ghost box.
    '''
    if ( pygame.time.get_ticks() - game_start_time) >= (len(ghosts_in_maze) + 1) * GHOST_RELEASE_DELAY:
        ghost_to_release = ghosts_not_in_maze.pop()
        ghost_to_release.in_maze = True
        ghosts_in_maze.append(ghost_to_release)



def game_won():
    ''' Function to exit the game if game is won'''
    window_surface.blit(you_win_image , you_win_position)
    pygame.display.update()
    pygame.time.delay(5000)
    exit(0)



def game_over(game_over_image , game_over_position):
    ''' Function to exit the game after game is over.'''
    window_surface.blit(game_over_image , game_over_position)   
    pygame.display.update()
    pygame.time.delay(5000)
    exit(0)



def check_ghost_collision(pacman , ghost):
    '''
    Checks collision of pacman and a single ghost.
    Parameters-
        pacman - Pacman object.
        ghost - Ghost object.
    Returns-
        bool - True if there is a collision , False otherwise.
    '''
    pacman_x_index = round(pacman.x / CELL_WIDTH)
    pacman_y_index = round(pacman.y / CELL_HEIGHT)

    ghost_x_index = round(ghost.x / CELL_WIDTH)
    ghost_y_index = round(ghost.y / CELL_HEIGHT)

    if(ghost_x_index == pacman_x_index and ghost_y_index == pacman_y_index):
        return True



def check_ghosts_collision(pacman , ghosts_in_maze):
    '''
    Checks collision of all the ghosts with pacman in the given array.
    Parameter-
        pacman - Pacman object.
        ghosts_in_maze - list of Ghost objects which are in the maze.
    Returns-
        bool - True if any ghost collides with pacman , False otherwise.
    '''

    for ghost in ghosts_in_maze:
        if check_ghost_collision(pacman , ghost):
            return True
    return False



def reinitialise(new_life_count):
    '''
    Re-initialises the game with the given life count.
    Parameters-
        life_count - the new life_count.
    '''

    global pacman , ghosts_in_maze , ghosts_not_in_maze , game_running , life_count , game_start_time

    pacman = Pacman.Pacman(336 , 504)
    ghosts_not_in_maze = [ Ghost.Ghost(
                        os.path.join(os.getcwd() , 'res' , 'tiles' , 'ghost-{}.gif'.format(ghost_name)),
                         13 * 24 , 13 * 24) for ghost_name in [ "sue",
                                                                "inky",
                                                                "pinky",
                                                                "blinky"]]
    ghosts_in_maze = []
    game_running = False
    life_count = new_life_count
    game_start_time = float('inf')






# Initialising the screen.
window_surface = pygame.display.set_mode( ( WINDOW_WIDTH , WINDOW_HEIGHT) )
pygame.display.set_caption(CAPTION)

# Game Objects.
clock = pygame.time.Clock()
maze = Maze.Maze( os.path.join(os.getcwd() , "res" , "levels" , "{}.json".format(LEVEL)))
pacman = Pacman.Pacman(336 , 504)
ghosts_not_in_maze = [ Ghost.Ghost(
                        os.path.join(os.getcwd() , 'res' , 'tiles' , 'ghost-{}.gif'.format(ghost_name)),
                         13 * 24 , 13 * 24) for ghost_name in [ "sue",
                                                                "inky",
                                                                "pinky",
                                                                "blinky"]]
# Setting AI level of the ghosts.
ghosts_not_in_maze[0].AI_level = 50
ghosts_not_in_maze[1].AI_level = 15
ghosts_not_in_maze[2].AI_level = 5
ghosts_not_in_maze[3].AI_level = 0

ghosts_in_maze = []


# Logos, other images and game variables.
game_running = False
game_start_time = float('inf')
life_count = 3

pacman_logo_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'logo.gif')).convert()
pacman_logo_position = [CELL_WIDTH * maze.x_length , CELL_HEIGHT]

ready_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'ready.gif')).convert()
ready_position = [CELL_WIDTH * (maze.x_length + 3) , CELL_HEIGHT * 4]

press_enter_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'pressenter.gif')).convert()
press_enter_position = [CELL_WIDTH * (maze.x_length + 3) , CELL_HEIGHT * 6]

game_over_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'gameover1.gif')).convert()
game_over_position = [CELL_WIDTH * (maze.x_length + 3) , CELL_HEIGHT * 4]

you_win_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'youwin1.gif')).convert()
you_win_position = [CELL_WIDTH * (maze.x_length + 3) , CELL_HEIGHT * 4]

life_image = pygame.image.load(os.path.join(os.getcwd() , 'res', 'text', 'life.gif')).convert()
life_position = [CELL_WIDTH + 5 , CELL_HEIGHT * maze.y_length]



# Game Loop -
while True:

    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # Enter is not a inbuilt key type. So for checking enter.
        keys_pressed = pygame.key.get_pressed()

        # If a key is pressed, change direction of Pacman.
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if game_running and event.key == pygame.K_LEFT:
                pacman.change_direction('l' , maze)
            
            if game_running and event.key == pygame.K_RIGHT:
                pacman.change_direction('r' , maze)
            
            if game_running and event.key == pygame.K_UP:
                pacman.change_direction('u' , maze)
            
            if game_running and event.key == pygame.K_DOWN:
                pacman.change_direction('d' , maze)

            if not game_running and ( event.key == pygame.K_KP_ENTER or keys_pressed[13] ):
                game_running = True
                game_start_time = pygame.time.get_ticks()

    # Updating Logos and background.
    window_surface.fill(BLACK)
    window_surface.blit(pacman_logo_image , pacman_logo_position)
    if not game_running:
        window_surface.blit(ready_image,ready_position)
        window_surface.blit(press_enter_image,press_enter_position)
    for i in range(life_count):
        window_surface.blit(life_image , [ life_position[0] + 20 * i , life_position[1] ])


    # Updating different objects in the game
    maze.update(window_surface)
    pacman.update(window_surface , maze)
    for ghost in ghosts_not_in_maze:
        ghost.update(window_surface , maze , pacman)
    for ghost in ghosts_in_maze:
        ghost.update(window_surface , maze , pacman)


    # Update the screen.
    pygame.display.update()

    # Check for collision with ghost.
    if check_ghosts_collision(pacman , ghosts_in_maze):
        if life_count == 0:
            game_over(game_over_image , game_over_position)

        reinitialise(life_count - 1)


    # Check if all the pellets are gone.
    if check_win(maze):
        game_won()

    # Release 1 ghost in the maze after every 5 second. if there is a ghost to release.
    if len(ghosts_not_in_maze) > 0:
        release_ghost_in_maze(ghosts_in_maze , ghosts_not_in_maze , game_start_time)


    clock.tick(FPS)     # Maintains the fps at a particular value.
