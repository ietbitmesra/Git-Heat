'''
This class is used to store data about the maze.
The matrix contains strings which refer to the image in the tile folder.
'''

import pygame

import json

import os

class Maze():

    
    def __init__(self , matrix_data_path):
        '''
        Initialises the maze. 
        Loads the maze information from matrix_data_path.
        
        Parameters-
            (string) matrix_data_path - Location of the json file to get matrix data.
        '''

        # Check if given path exists.
        if not os.path.exists(matrix_data_path):
            raise Exception("File does not exist : {}".format(matrix_data_path))

        # 2D array containing information of each cell i.e. what image is to be drawn.
        with open(matrix_data_path , "r") as matrix_file:
            self.matrix = json.load(matrix_file)

        self.cell_width = 24    # Width of each cell.
        self.cell_height = 24   # Height of each cell.
        self.x_length = len(self.matrix[0]) # Number of columns. 
        self.y_length = len(self.matrix)    # Number of rows.

        self.images , self.positions = self.get_images_positions()


    def get_images_positions(self):
        '''
        Loads all the tile images from local directory and also store all the (x,y) position for each cell.

        Returns-
            images (images of all the cells) , positions ((x,y) position of all the cells).
        '''
        images = [[0 for i in range(self.x_length)] for j in range(self.y_length)]
        positions = [[0 for i in range(self.x_length)] for j in range(self.y_length)]

        for y in range(self.y_length):
            for x in range(self.x_length):
                if "pellet" in self.matrix[y][x]:
                    file_name = self.matrix[y][x]+".png"
                else:
                    file_name = self.matrix[y][x]+".gif"
                images[y][x] = pygame.image.load(os.path.join(os.getcwd() , "res" , "tiles" , file_name)).convert()
                positions[y][x] = [x * self.cell_width , y * self.cell_height]

        return images , positions


    def update(self , window_surface):
        ''' Update the screen with all the walls '''

        for y in range(self.y_length):
            for x in range(self.x_length):
                window_surface.blit(self.images[y][x] , self.positions[y][x])

    