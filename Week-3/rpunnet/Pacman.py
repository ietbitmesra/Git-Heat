"""
The class here contains information about pacman and its properties.
"""

import pygame

import os    

from math import ceil , floor

class Pacman():
    
    def __init__(self , pos_x , pos_y):
        '''
        Initialises pacman object at (pos_x , pos_y) with default values.

        Parameters-
            (float) pos_x - Initial x position of pacman.
            (float) pos_y - Initial y position of pacman.
        '''

        self.x = pos_x
        self.y = pos_y

        self.x_vel = 0
        self.y_vel = 1
        
        # l - left , u - up , r - right , d - down.
        self.direction = 'd'
        # frame number goes from 1 to 8 to load the respective image on screen for animation
        self.frame_number = 0
        # frame skip is the number of frames to skip before drawing the next sprite.
        self.frame_skip = 10
        
        self.images = self.get_images()

    def get_images(self):
        '''
        Loads all the pacman sprites from the local directory.
        
        Returns - 
            images - Different images of pacman for each frame 
                        and different orientations.
        '''

        path = os.path.join(os.getcwd() , "res" , "sprite")
        images = {'l':[] , 'r':[] , 'd':[] , 'u':[]}
        
        for i in range(1 ,9):
            for dir in images:
                images[dir].append(
                    pygame.image.load(
                        os.path.join(path , "pacman-{} {}.gif".format(dir , i))
                                    ).convert()
                                )

        return images

    def update(self , window_surface , maze):
        '''
        Updates the pacman sprite on the screen.
        
        Parameters-
            window_surface - Screen where pacman has to be updated.
            maze - Maze object for checking any collisions.
        '''
        if self.frame_number >= (8 * self.frame_skip ):
            self.frame_number = 0

        image = self.images[self.direction][self.frame_number // self.frame_skip]
        position = [self.x , self.y]
        window_surface.blit(image , position)

        # Check for Pellet at current psition.
        if "pellet" in maze.matrix[round(self.y / 24)][round(self.x / 24)]:
            self.eat_pellet(maze)

        self.move(maze)   # Change the x and y position of pacman according to the direction

    def eat_pellet(self , maze):
        maze.matrix[round(self.y / 24)][round(self.x / 24)] = "blank"
        maze.images[round(self.y / 24)][round(self.x / 24)] =  pygame.image.load(os.path.join(os.getcwd() , "res" , "tiles" , "blank.gif")).convert()

    
    def get_index_maze(self , pos_x , pos_y):
        '''
        Gets the index of the next cell in maze to check for collisions.
        Parameters - 
            pos_x - x co-ordinate.
            pos_y - y co-ordinate.
        Returns-
            x_index ( index of column ) , y_index (index of row).
        '''

        x_index , y_index = 0 , 0
        
        if self.x_vel == 1:
            x_index = ceil(pos_x/24)
        else:
            x_index = floor(pos_x/24)
        
        if self.y_vel == 1:
            y_index = ceil(pos_y/24)
        else:
            y_index = floor(pos_y/24)

        return x_index , y_index

    def move(self , maze):
        '''
        Updates the (x,y) position of pacman according to the direction
        and also checks for collision with wall.
        
        Parameters-
            maze - Maze object for checking wall positions.
        '''
        new_x = self.x + self.x_vel
        new_y = self.y + self.y_vel

        # Check for teleporter on left side.
        if new_x < 24:
            new_x = 24 * ( maze.x_length - 2)
        # Check for teleporter on right side.
        if new_x > 24 * ( maze.x_length - 2):
            new_x = 24        

        x_index , y_index = self.get_index_maze(new_x , new_y)
        
        if "wall" in maze.matrix[y_index][x_index]:
            return
        
        self.x = new_x
        self.y = new_y

        self.frame_number += 1


    def change_direction(self , dir , maze):
        '''
        Change the direction pacman is moving in.
        If the new direction contains wall then doesn't change the direction.
        
        Parameters -
            dir - The new direction.
            maze - Maze object for checking walls.
        '''
        index_x = round(self.x / 24)
        index_y = round(self.y / 24)
        
        
        if dir == 'l':
            if "wall" in maze.matrix[index_y][index_x - 1]:
                return
            self.x_vel = -1
            self.y_vel = 0
            self.y = index_y * 24
            self.direction = dir

        elif dir == 'r':
            if "wall" in maze.matrix[index_y][index_x + 1]:
                return
            self.x_vel = 1
            self.y_vel = 0
            self.y = index_y * 24
            self.direction = dir

        elif dir == 'd':
            if "wall" in maze.matrix[index_y + 1][index_x]:
                return
            self.x_vel = 0
            self.y_vel = 1
            self.x = index_x * 24
            self.direction = dir
        
        elif dir == 'u':
            if "wall" in maze.matrix[index_y - 1][index_x]:
                return
            self.x_vel = 0
            self.y_vel = -1
            self.x = index_x * 24
            self.direction = dir

        else:
            raise Exception("Incorrect direction.")