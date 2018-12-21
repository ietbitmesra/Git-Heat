'''
A library for Ghost objects. It holds there information and other data.
'''

import pygame

import os

import GhostAI

from math import ceil , floor



class Ghost:

    def __init__(self , image_path , pos_x , pos_y):
        '''
        Initialises a ghost in the ghost room.

        Parameters-
            image_path - Loads ghost's image from the image_path.
            pos_x - Initial x position of ghost.
            pos_y - Initial y position of ghost.
        '''
        self.x = pos_x
        self.y = pos_y

        self.x_vel = 1
        self.y_vel = 0
        
        # l - left , u - up , r - right , d - down.
        self.direction = 'd'

        # Bool value to check if ghost is in maze or not.
        self.in_maze = False

        self.AI_level = 0

        self.image = pygame.image.load(image_path)
    

    def update(self , window_surface , maze , pacman):
        '''
        Updates the ghodt sprite on the screen.
        
        Parameters-
            window_surface - Screen where ghost has to be updated.
            maze - Maze object for checking any collisions.
        '''

        window_surface.blit(self.image , [self.x , self.y])

        self.move(maze , pacman)   # Change the x and y position of ghost according to the direction

    
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

    def check_wall_collision(self , maze , x_index , y_index):
        ''' 
        Checks for collision with any wall in the direction ghost is moving.
        The ghost box door is considered a one way wall.

        Parameters-
            maze - Maze object for checking cells.
            x_index - column index in maze.matrix of next cell.
            y_index - row index in maze.matrix of next cell.
        Returns-
            bool - True if the next cell contains a wall.
        '''

        # If ghost is not in maze.
        if self.in_maze == False:
            return "wall" in maze.matrix[y_index][x_index]
        
        # Checking if ghost is trying to go out of the maze.
        if self.direction == 'u':
            return "wall" in maze.matrix[y_index][x_index] and "ghost" not in maze.matrix[y_index][x_index]
        
        # If ghost is out of the maze the ghost wall is considered a wall.
        return "wall" in maze.matrix[y_index][x_index]

    def in_ghost_box(self , maze):
        ''' Returns True if ghost is inside the ghost box.'''
        return (self.x <= (16 * maze.cell_width) and 
                self.x >= (10 * maze.cell_width) and
                self.y <= (15 * maze.cell_height) and 
                self.y >= (11 * maze.cell_height) 
                )

    def at_cell(self , maze):
        ''' Returns True if ghost is perfectly present at a cell'''
        return self.x % maze.cell_width == 0 and self.y % maze.cell_height == 0

    def move(self , maze , pacman):
        '''
        Updates the (x,y) position of ghost according to the direction
        and also checks for collision with wall.
        If there is a collision change the direction.
        
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

        # Changing direction after collision with a wall.
        if self.check_wall_collision(maze , x_index , y_index):
            if self.in_maze == False or self.in_ghost_box(maze):
                new_direction = GhostAI.get_direction(pacman , maze , self , 0)
            else:
                new_direction = GhostAI.get_direction(pacman , maze , self , self.AI_level)
            if new_direction != 'none':
                self.change_direction(new_direction , maze)
                return
        
        # Changing direction on a 3-way or 4-way.
        if not self.in_ghost_box(maze) and self.at_cell(maze):
            new_direction = GhostAI.get_direction(pacman , maze , self , self.AI_level)
            dirs = [set(['l' , 'r']) , set(['u' , 'd'])]

            if new_direction != 'none' and new_direction != self.direction and set([new_direction , self.direction]) not in dirs:
                old_direction = self.direction
                self.change_direction(new_direction , maze)
                temp_new_x = self.x + self.x_vel
                temp_new_y = self.y + self.y_vel
                temp_x_index , temp_y_index = self.get_index_maze(new_x , new_y)
                if not self.check_wall_collision(maze , x_index , y_index):
                    new_x = temp_new_x
                    new_y = temp_new_y
                else:
                    self.change_direction(old_direction , maze)

        self.x = new_x
        self.y = new_y

    
    def change_direction(self , dir , maze):
        '''
        Change the direction ghost is moving in.
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