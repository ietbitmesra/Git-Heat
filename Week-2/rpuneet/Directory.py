'''
This  contains a class Directory which contains informations about that directory.
'''

import os

import File   # For storing files.


class Directory:
    
    '''
    Parameters:
        (string) path - The path of the directory.[example - "D/folder1/games" is the path for games directory]
    '''
    def __init__(self , path):
        self.path = path
        self.name = ""

        # Check for any problem in openning the directory. (Like - Permission denied.)
        try:
            os.listdir(self.path)
            self.name = os.path.basename(self.path)
        except IOError as e:
            print (e)
            self.path = None
            
        
    '''
    Returns the directory_list and file list.
    The fist index of file_list and directory_list will contain the count.
    
    Returns:
        (tuple of lists) - (directory_list , file_list)
    '''
    def get_children_list(self):
        all_dirs_files = os.listdir(self.path)
        directory_list = []
        file_list = []
        directory_count = [0]
        file_count = [0]
        
        for obj in all_dirs_files:
            obj_path = os.path.join(self.path , obj)
            if os.path.isdir(obj_path):
                directory_list.append(Directory(obj_path))
                directory_count[0] += 1
            else:
                file_list.append(File.File(obj_path))
                file_count[0] += 1
                
        return (directory_count + directory_list , file_count + file_list)
        
        
    '''
    It recursively visits each subdirectory and reads all the file to get the size of the directory.
    
    Returns - 
        the size of the directory , number of sub directories(recursively) and number of file(recursively). 
    
    '''
    def get_stats(self):
        if self.path == None:
            return (0 , 0 , 0)
        size = 0
        directory_list , file_list = self.get_children_list()
        size = 0
        directory_count = 0
        file_count = 0
        for directory in directory_list[1:]:
            tup_obj = directory.get_stats()

            file_count += tup_obj[2]

            directory_count += tup_obj[1]
            directory_count += 1

            size += tup_obj[0]
            
        for file in file_list[1:]:
            size += file.get_size()
            file_count += 1
        
        return (size , directory_count , file_count)