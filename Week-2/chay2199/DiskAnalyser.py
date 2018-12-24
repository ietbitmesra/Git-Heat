
# coding: utf-8

# In[ ]:


import os
import sys
import platform
import ctypes
import psutil
import matplotlib.pyplot as plt



####################################For Linux###############################
                
if(platform.system() == 'Linux'):
    
    
    print('Enter -1 to kill the program or -2 to know ' 
          'the details about that folder or -3 to go back '
          'to the root directory or the index number '
          'to further enter in a directory. Please note that if your using'
          ' a linux based system like Ubuntu then you can enter'
          ' all your other disks from /media/ ')
    print('##################################################')
    print('You are currently in "/"')
    print('##################################################')
    print('These are all the files and folders in your system: ')
    index = 0
    dirlist = []
    pathName = '/'

    try:
        for x in os.listdir(pathName):
            dirlist.append(x)
            if os.path.isfile(x): print (index,"  ",'f-', x)
            elif os.path.isdir(x): print (index,"  ",'d-', x)
            elif os.path.islink(x): print (index,"  ",'l-', x)
            else: print (index,"  ", x)
            index = index + 1
        choice = int(input())

    except NotADirectoryError:
        print('Oops the index you have selected is of a file. You can try again!!')

        statinfo = os.stat(pathName[:-1])
        fileSize = statinfo.st_size/(1000000)
        print('Your file size in MB: ',fileSize)

        print('Enter -1 to kill the program or -2 to know ' 
          'the details about that folder or -3 to go back '
          'in the parent directory or the index number '
          'to further enter in a directory.')
        choice = int(input())


    if(choice == -3):
        print('You are currently in the root directory. You cannot go back.')
        print('Enter -1 to kill the program or -2 to know ' 
          'the details about that folder or -3 to go back '
          'in the parent directory or the index number '
          'to further enter in a directory.')
        choice = int(input())




    if(choice == -2):
        try:
            stat = os.statvfs(pathName)
            freeSpace = stat.f_bfree*stat.f_bsize/(1000000)

            folder = pathName
            folder_size = 0
            for (path, dirs, files) in os.walk(folder):
                for file in files:
                    filename = os.path.join(path, file)
                    try:
                        folder_size += os.path.getsize(filename)
                    except FileNotFoundError:
                        print('Oops file not found! Maybe there is a broken file in there. '
                              'Please check and try again')
                        print('Your directory is: ',pathName)
                        print('Enter -1 to kill the program or -2 to know ' 
                              'the details about that folder or -3 to go back '
                              'in the parent directory or the index number '
                              'to further enter in a directory.')
                        choice = int(input())

                    except PermissionError:
                        print('Oops permission eroor! You dont have the permission to access '
                              'the file. Please check and try again')
                        print('Your directory is: ',pathName)
                        print('Enter -1 to kill the program or -2 to know ' 
                              'the details about that folder or -3 to go back '
                              'in the parent directory or the index number '
                              'to further enter in a directory.')
                        choice = int(input())

            folderSize = folder_size/1000000

            labels = 'Used Space', 'Free Space'
            sizes = [folderSize, freeSpace]
            cols = ['r', 'g']
            plt.pie(sizes, labels = labels, colors=cols, shadow = True,
                    explode = (0, 0.075), autopct='%1.2f%%')

            print('Your directory is: ',pathName)
            print('Details of the current directory are: ')
            print('######################################')
            print('Used Space in MB: ',folderSize," ",'Free Space in MB: ',freeSpace)
            plt.show()

            choice = int(input())

        except NotADirectoryError:
                print('The index you have selected is of a file.')
                folder = pathName
                folder_size = 0
                for (path, dirs, files) in os.walk(folder):
                    for file in files:
                        filename = os.path.join(path, file)
                        folder_size += os.path.getsize(filename)

                folderSize = folder_size/(1000000)
                print('Your file size in MB: ',folderSize)


                choice = int(input())



    while(choice != -1):

        if(choice == -3):
                print('You are currently in the root directory.')
                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'in the parent directory or the index number '
                      'to further enter in a directory.')

                index = 0
                dirlist = []
                pathName = '/'

                try:
                    for x in os.listdir(pathName):
                        dirlist.append(x)
                        if os.path.isfile(x): print (index,"  ",'f-', x)
                        elif os.path.isdir(x): print (index,"  ",'d-', x)
                        elif os.path.islink(x): print (index,"  ",'l-', x)
                        else: print (index,"  ", x)
                        index=index+1
                    choice = int(input())

                except NotADirectoryError:
                    print('Oops the index you have selected is of a file. You can try again!!')
                    print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'in the parent directory or the index number '
                      'to further enter in a directory.')
                    choice = int(input())




        if(choice == -2):
            try:
                stat = os.statvfs(pathName)
                freeSpace = stat.f_bfree*stat.f_bsize/(1000000)



                folder = pathName
                folder_size = 0
                for (path, dirs, files) in os.walk(folder):
                    for file in files:
                        filename = os.path.join(path, file)
                        try:
                            folder_size += os.path.getsize(filename)
                        except FileNotFoundError:
                            print('Oops file not found! Maybe there is a broken file in there. '
                                  'Please check and try again')
                            print('Your directory is: ',pathName)
                            print('Enter -1 to kill the program or -2 to know ' 
                                  'the details about that folder or -3 to go back '
                                  'in the parent directory or the index number '
                                  'to further enter in a directory.')
                            choice = int(input())

                        except PermissionError:
                            print('Oops permission eroor! You dont have the permission to access '
                                  'the file. Please check and try again')
                            print('Your directory is: ',pathName)
                            print('Enter -1 to kill the program or -2 to know ' 
                                  'the details about that folder or -3 to go back '
                                  'in the parent directory or the index number '
                                  'to further enter in a directory.')
                            choice = int(input())

                folderSize = folder_size/(1000000)

                labels = 'Used Space', 'Free Space'
                sizes = [folderSize, freeSpace]
                cols = ['r', 'g']
                plt.pie(sizes, labels = labels, colors = cols, shadow = True,
                        explode = (0, 0.075), autopct='%1.2f%%')
                print('Your directory is: ',pathName)
                print('Details of the current directory are: ')
                print('######################################')
                print('Used Space in MB: ',folderSize," ",'Free Space in MB: ',freeSpace)
                plt.show()


                choice = int(input())

            except NotADirectoryError:
                print('The index you have selected is of a file.')
                statinfo = os.stat(pathName[:-1])
                fileSize = statinfo.st_size/(1000000)
                print('Your file size in MB: ',fileSize)


                choice = int(input())


        if(choice >= 0):
            index = 0
            pathName = pathName + str(dirlist[choice]) + '/'
            dirlist = []
            print('You are currently in ',pathName)
            print('#####################################')
            print('#####################################')
            print('#####################################')
            print('#####################################')
            print('#####################################')

            try:
                print('These are all the files and folders in this directory: ')
                for x in os.listdir(pathName):
                    dirlist.append(x)
                    if os.path.isfile(x): print (index,"  ",'f-', x)
                    elif os.path.isdir(x): print (index,"  ",'d-', x)
                    elif os.path.islink(x): print (index,"  ",'l-', x)
                    else: print (index,"  ", x)
                    index = index+1
                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'in the parent directory or the index number '
                      'to further enter in a directory.')
                print('##################################################')
                print('##################################################')
                print('##################################################')
                print('##################################################')
                choice = int(input())

            except NotADirectoryError:
                print('Oops the index you have selected is of a file. You can try again!!')

                statinfo = os.stat(pathName[:-1])
                fileSize=statinfo.st_size/(1000000)
                print('Your file size in MB: ',fileSize)

                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or the index number '
                      'to further enter in a directory.')
                choice = int(input())


########################################FOR WINDOWS#################            

elif(platform.system() == 'Windows'):
    
    
    import win32api
        
    
    
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    windowsDrives = []
    for drive in drives:
        windowsDrives.append(drive[:-1])
    
    print('These are the drives in your system: ',windowsDrives)
    print('Please enter a number to choose your parent directory')
    print('REMEMEBER the index starts from zero')
    
    dir = int(input())
    
    if(dir < len(windowsDrives)):
        parentDir = windowsDrives[dir] + '/'
        pathName = windowsDrives[dir] + '/'
    else:
        while(dir >= len(windowsDrives)):
            print('Invalid parent directory. Please try again!')
            print('These are the drives in your system: ',windowsDrives)
            print('Please enter a number to choose your parent directory')
            print('REMEMEBER the index starts from zero')

            dir = int(input())
        parentDir = windowsDrives[dir] + '/'
        pathName = windowsDrives[dir] + '/'
        
    
    
    print('Enter -1 to kill the program or -2 to know ' 
              'the details about that folder or -3 to go back '
              'to the parent directory or -4 to change parent'
              ' directory or the index number '
              'to further enter in a directory.')
    print('##################################################')
    print('You are currently in this directory: ', pathName)
    print('##################################################')
    print('These are all the files and folders in your system: ')
    index = 0
    dirlist = []
    try:
        for x in os.listdir(pathName):
            dirlist.append(x)
            if os.path.isfile(x): print (index,"  ",'f-', x)
            elif os.path.isdir(x): print (index,"  ",'d-', x)
            elif os.path.islink(x): print (index,"  ",'l-', x)
            else: print (index,"  ", x)
            index = index+1
        choice = int(input())

    except NotADirectoryError:
        print('Oops the index you have selected is of a file. You can try again!!')

        statinfo = os.stat(pathName[:-1])
        fileSize = statinfo.st_size/(1000000)
        print('Your file size in MB: ',fileSize)

        print('Enter -1 to kill the program or -2 to know ' 
              'the details about that folder or -3 to go back '
              'to the parent directory or -4 to change parent'
              ' directory.')
        choice = int(input())

    
    if(choice == -4):
        print('These are the drives in your system: ',windowsDrives)
        print('Please enter a number to choose your parent directory')
        print('REMEMEBER the index starts from zero')

        dir = int(input())

        if(dir < len(windowsDrives)):
            parentDir = windowsDrives[dir] + '/'
            pathName = windowsDrives[dir] + '/'
        else:
            while(dir >= len(windowsDrives)):
                print('Invalid parent directory. Please try again!')
                print('These are the drives in your system: ',windowsDrives)
                print('Please enter a number to choose your parent directory')
                print('REMEMEBER the index starts from zero')

                dir = int(input())
            parentDir = windowsDrives[dir] + '/'
            pathName = windowsDrives[dir] + '/'



        print('Enter -1 to kill the program or -2 to know ' 
              'the details about that folder or -3 to go back '
              'to the parent directory or -4 to change parent'
              ' directory or the index number '
              'to further enter in a directory.')
        print('##################################################')
        print('You are currently in this directory: ', pathName)
        print('##################################################')
        print('These are all the files and folders in your system: ')
        
        index = 0
        dirlist = []
        try:
            for x in os.listdir(pathName):
                dirlist.append(x)
                if os.path.isfile(x): print (index,"  ",'f-', x)
                elif os.path.isdir(x): print (index,"  ",'d-', x)
                elif os.path.islink(x): print (index,"  ",'l-', x)
                else: print (index,"  ", x)
                index = index+1
            choice = int(input())

        except NotADirectoryError:
            print('Oops the index you have selected is of a file. You can try again!!')

            statinfo = os.stat(pathName[:-1])
            fileSize = statinfo.st_size/(1000000)
            print('Your file size in MB: ',fileSize)

            print('Enter -1 to kill the program or -2 to know ' 
                  'the details about that folder or -3 to go back '
                  'to the parent directory or -4 to change parent'
                  ' directory.')
            choice = int(input())
        
    
    if(choice == -3):
        print('You are currently in the parent directory. You cannot go back.')
        print('Enter -1 to kill the program or -2 to know ' 
          'the details about that folder or the index number '
          'to further enter in a directory or -4 to change your parent directory.')
        choice = int(input())




    if(choice == -2):
        try:
            freeSpace = psutil.disk_usage(pathName).free/1000000

            folder = pathName
            folder_size = 0
            for (path, dirs, files) in os.walk(folder):
                for file in files:
                    filename = os.path.join(path, file)
                    try:
                        folder_size += os.path.getsize(filename)
                    except FileNotFoundError:
                        print('Oops file not found! Maybe there is a broken file in there. '
                              'Please check and try again')
                        print('Your directory is: ',pathName)
                        print('Enter -1 to kill the program or -2 to know ' 
                              'the details about that folder or -3 to go back '
                              'to the parent directory or -4 to change parent'
                              ' directory.')
                        choice = int(input())

                    except PermissionError:
                        print('Oops permission error! You dont have the permission to access '
                              'the file. Please check and try again')
                        print('Your directory is: ',pathName)
                        print('Enter -1 to kill the program or -2 to know ' 
                              'the details about that folder or -3 to go back '
                              'to the parent directory or -4 to change parent'
                              ' directory.')
                        choice = int(input())

            folderSize = folder_size/1000000

            labels = 'Used Space', 'Free Space'
            sizes = [folderSize, freeSpace]
            cols = ['r', 'g']
            plt.pie(sizes, labels = labels, colors=cols, shadow = True,
                    explode = (0, 0.075), autopct='%1.2f%%')

            print('Your directory is: ',pathName)
            print('Details of the current directory are: ')
            print('######################################')
            print('Used Space in MB: ',folderSize," ",'Free Space in MB: ',freeSpace)
            plt.show()

            choice = int(input())

        except NotADirectoryError:
                print('The index you have selected is of a file.')
                folder = pathName
                folder_size = 0
                for (path, dirs, files) in os.walk(folder):
                    for file in files:
                        filename = os.path.join(path, file)
                        folder_size += os.path.getsize(filename)

                folderSize=folder_size/(1000000)
                print('Your file size in MB: ',folderSize)


                choice = int(input())



    while(choice != -1):
        
        
        if(choice == -4):
            print('These are the drives in your system: ',windowsDrives)
            print('Please enter a number to choose your parent directory')
            print('REMEMEBER the index starts from zero')

            dir = int(input())

            if(dir < len(windowsDrives)):
                pathName = windowsDrives[dir] + '/'
                parentDir = windowsDrives[dir] + '/'
            else:
                while(dir >= len(windowsDrives)):
                    print('Invalid parent directory. Please try again!')
                    print('These are the drives in your system: ',windowsDrives)
                    print('Please enter a number to choose your parent directory')
                    print('REMEMEBER the index starts from zero')

                    dir = int(input())
                pathName = windowsDrives[dir] + '/'
                parentDir = windowsDrives[dir] + '/'



            print('Enter -1 to kill the program or -2 to know ' 
                  'the details about that folder or -3 to go back '
                  'to the parent directory or -4 to change parent'
                  ' directory or the index number '
                  'to further enter in a directory.')
            print('##################################################')
            print('You are currently in this directory: ', pathName)
            print('##################################################')
            print('These are all the files and folders in your system: ')
            
            index = 0
            dirlist = []
            try:
                for x in os.listdir(pathName):
                    dirlist.append(x)
                    if os.path.isfile(x): print (index,"  ",'f-', x)
                    elif os.path.isdir(x): print (index,"  ",'d-', x)
                    elif os.path.islink(x): print (index,"  ",'l-', x)
                    else: print (index,"  ", x)
                    index = index+1
                choice = int(input())

            except NotADirectoryError:
                print('Oops the index you have selected is of a file. You can try again!!')

                statinfo = os.stat(pathName[:-1])
                fileSize = statinfo.st_size/(1000000)
                print('Your file size in MB: ',fileSize)

                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'to the parent directory or -4 to change parent'
                      ' directory.')
                choice = int(input())

        if(choice == -3):
                print('You are currently in the parent directory.')
                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'in the parent directory or -4 to change the'
                      ' parent directory or the index number '
                      'to further enter in a directory.')

                index = 0
                dirlist = []
                pathName = parentDir

                try:
                    for x in os.listdir(pathName):
                        dirlist.append(x)
                        if os.path.isfile(x): print (index,"  ",'f-', x)
                        elif os.path.isdir(x): print (index,"  ",'d-', x)
                        elif os.path.islink(x): print (index,"  ",'l-', x)
                        else: print (index,"  ", x)
                        index = index+1
                    choice = int(input())

                except NotADirectoryError:
                    print('Oops the index you have selected is of a file. You can try again!!')
                    print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'in the parent directory.')
                    choice = int(input())




        if(choice == -2):
            try:
                freeSpace = psutil.disk_usage(pathName).free/1000000
                
                folder = pathName
                folder_size = 0
                for (path, dirs, files) in os.walk(folder):
                    for file in files:
                        filename = os.path.join(path, file)
                        try:
                            folder_size += os.path.getsize(filename)
                        except FileNotFoundError:
                            print('Oops file not found! Maybe there is a broken file in there. '
                                  'Please check and try again')
                            print('Your directory is: ',pathName)
                            print('Enter -1 to kill the program or -2 to know ' 
                                  'the details about that folder or -3 to go back '
                                  'to the parent directory or -4 to change parent'
                                  ' directory.')
                            choice = int(input())

                        except PermissionError:
                            print('Oops permission error! You dont have the permission to access '
                                  'the file. Please check and try again')
                            print('Your directory is: ',pathName)
                            print('Enter -1 to kill the program or -2 to know ' 
                                  'the details about that folder or -3 to go back '
                                  'to the parent directory or -4 to change parent'
                                  ' directory.')
                            choice = int(input())

                folderSize = folder_size/(1000000)

                labels = 'Used Space', 'Free Space'
                sizes = [folderSize, freeSpace]
                cols = ['r', 'g']
                plt.pie(sizes, labels = labels, colors=cols, shadow = True,
                        explode = (0, 0.075), autopct='%1.2f%%')
                print('Your directory is: ',pathName)
                print('Details of the current directory are: ')
                print('######################################')
                print('Used Space in MB: ',folderSize," ",'Free Space in MB: ',freeSpace)
                plt.show()


                choice = int(input())

            except NotADirectoryError:
                print('The index you have selected is of a file.')
                statinfo = os.stat(pathName[:-1])
                fileSize=statinfo.st_size/(1000000)
                print('Your file size in MB: ',fileSize)


                choice = int(input())


        if(choice >= 0):
            index = 0
            pathName = pathName+str(dirlist[choice]) + '/'
            dirlist = []
            print('You are currently in ',pathName)
            print('#####################################')
            print('#####################################')
            print('#####################################')
            print('#####################################')
            print('#####################################')

            try:
                print('These are all the files and folders in this directory: ')
                for x in os.listdir(pathName):
                    dirlist.append(x)
                    if os.path.isfile(x): print (index,"  ",'f-', x)
                    elif os.path.isdir(x): print (index,"  ",'d-', x)
                    elif os.path.islink(x): print (index,"  ",'l-', x)
                    else: print (index,"  ", x)
                    index = index+1
                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back '
                      'to the parent directory or -4 to change parent'
                      ' directory or the index number '
                      'to further enter in a directory.')
                print('##################################################')
                print('##################################################')
                print('##################################################')
                print('##################################################')
                choice = int(input())

            except NotADirectoryError:
                print('Oops the index you have selected is of a file. You can try again!!')

                statinfo = os.stat(pathName[:-1])
                fileSize = statinfo.st_size/(1000000)
                print('Your file size in MB: ',fileSize)

                print('Enter -1 to kill the program or -2 to know ' 
                      'the details about that folder or -3 to go back to the root directory'
                      ' or -4 to change the parent directory')
                choice = int(input())




