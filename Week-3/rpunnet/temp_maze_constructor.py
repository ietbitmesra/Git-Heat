''' This file is used to create the maze i.e. 1.json file for loading a level'''

import json

n = 28
m = 26

data = [["blank" for i in range(m)] for j in range(n)]
data[1][1] = "wall-corner-ul"
data[1][m-1] = "wall-corner-ur"

for i in range(2 , m-1):
    data[1][i] = "wall-straight-horiz"
data[1][m//2] = "wall-t-top"

for i in range(2 , 10):
    data[i][1] = "wall-straight-vert"
data[10][1] = "wall-corner-ll"

for i in range(2 , 6):
    data[10][i] = "wall-straight-horiz"
data[10][6] = "wall-corner-ur"
data[11][6] = "wall-straight-vert"
data[12][6] = "wall-corner-lr"
for i in range(1 , 6):
    data[12][i] = "wall-straight-horiz"

for i in range(1 , 6):
    data[14][i] = "wall-straight-horiz"
data[14][6] = "wall-corner-ur"
data[15][6] = "wall-straight-vert"
data[16][6] = "wall-corner-lr"

for i in range(2 , 6):
    data[16][i] = "wall-straight-horiz"
data[16][1] = "wall-corner-ul"

for i in range(17 , n-1):
    data[i][1] = "wall-straight-vert"
data[n-1][1] = "wall-corner-ll"





data[n-1][m-1] = "wall-corner-lr"

for i in range(2 , m-1):
    data[n-1][i] = "wall-straight-horiz"
data[n-1][m//2] = "wall-straight-horiz"

for i in range(2 , 10):
    data[i][m-1] = "wall-straight-vert"

data[10][m-1] = "wall-corner-lr"

for i in range(m-5 , m-1):
    data[10][i] = "wall-straight-horiz"
data[10][m-6] = "wall-corner-ul"
data[11][m-6] = "wall-straight-vert"
data[12][m-6] = "wall-corner-ll"
for i in range(1 , 6):
    data[12][m-i] = "wall-straight-horiz"

for i in range(1 , 6):
    data[14][m-i] = "wall-straight-horiz"
data[14][m-6] = "wall-corner-ul"
data[15][m-6] = "wall-straight-vert"
data[16][m-6] = "wall-corner-ll"

for i in range(2 , 6):
    data[16][m-i] = "wall-straight-horiz"
data[16][m-1] = "wall-corner-ur"

for i in range(17 , n-1):
    data[i][m-1] = "wall-straight-vert"


data[13][16] = "wall-straight-vert"
data[13][10] = "wall-straight-vert"
data[11][16] = "wall-end-t"
data[11][10] = "wall-end-t"
data[15][10] = "wall-corner-ll"
data[14][10] = "wall-straight-vert"
data[12][10] = "wall-straight-vert"
data[15][16] = "wall-corner-lr"
data[14][16] = "wall-straight-vert"
data[12][16] = "wall-straight-vert"

for i in range(11 , 16):
    data[11][i] = "ghost-wall"
    data[15][i] = "wall-straight-horiz"

data[17][10] = "wall-end-l"
data[17][16] = "wall-end-r"
for i in range(11 , 16):
    data[17][i] = "wall-straight-horiz"
data[17][13] = "wall-t-top"
data[18][13] = "wall-straight-vert"
data[19][13] = "wall-straight-vert"
data[20][13] = "wall-end-b"

data[22][10] = "wall-end-l"
data[22][16] = "wall-end-r"
for i in range(11 , 16):
    data[22][i] = "wall-straight-horiz"
data[22][13] = "wall-t-top"
data[23][13] = "wall-straight-vert"
data[24][13] = "wall-straight-vert"
data[25][13] = "wall-end-b"


data[6][10] = "wall-end-l"
data[6][16] = "wall-end-r"
for i in range(11 , 16):
    data[6][i] = "wall-straight-horiz"
data[6][13] = "wall-t-top"
data[7][13] = "wall-straight-vert"
data[8][13] = "wall-straight-vert"
data[9][13] = "wall-end-b"

data[4][13] = "wall-end-b"
data[3][13] = "wall-straight-vert"
data[2][13] = "wall-straight-vert"

# T right tilted
data[8][11] = "wall-corner-ur"
data[8][10] = "wall-straight-horiz"
data[8][9] = "wall-straight-horiz"
data[8][8] = "wall-t-left"
data[9][8] = "wall-t-left"
data[10][8] = "wall-straight-vert"
data[11][8] = "wall-straight-vert"
data[12][8] = "wall-end-b"
data[9][11] = "wall-corner-lr"
data[9][10] = "wall-straight-horiz"
data[9][9] = "wall-straight-horiz"
data[7][8] = "wall-straight-vert"
data[6][8] = "wall-end-t"

#T left tilted
data[8][15] = "wall-corner-ul"
data[8][16] = "wall-straight-horiz"
data[8][17] = "wall-straight-horiz"
data[8][18] = "wall-t-right"
data[9][18] = "wall-t-right"
data[10][18] = "wall-straight-vert"
data[11][18] = "wall-straight-vert"
data[12][18] = "wall-end-b"
data[9][15] = "wall-corner-ll"
data[9][16] = "wall-straight-horiz"
data[9][17] = "wall-straight-horiz"
data[7][18] = "wall-straight-vert"
data[6][18] = "wall-end-t"


data[4][11] = "wall-corner-lr"
data[3][11] = "wall-corner-ur"
data[4][10] = "wall-straight-horiz"
data[3][10] = "wall-straight-horiz"
data[4][9] = "wall-straight-horiz"
data[3][9] = "wall-straight-horiz"
data[4][8] = "wall-corner-ll"
data[3][8] = "wall-corner-ul"


data[4][15] = "wall-corner-ll"
data[3][15] = "wall-corner-ul"
data[4][16] = "wall-straight-horiz"
data[3][16] = "wall-straight-horiz"
data[4][17] = "wall-straight-horiz"
data[3][17] = "wall-straight-horiz"
data[4][18] = "wall-corner-lr"
data[3][18] = "wall-corner-ur"

# C and O left 
data[3][3] = "wall-end-l"
data[3][4] = "wall-straight-horiz"
data[3][5] = "wall-straight-horiz"
data[3][6] = "wall-corner-ur"
data[4][6] = "wall-straight-vert"
data[5][6] = "wall-straight-vert"
data[6][6] = "wall-straight-vert"
data[7][6] = "wall-straight-vert"
data[8][6] = "wall-corner-lr"
data[8][3] = "wall-end-l"
data[8][4] = "wall-straight-horiz"
data[8][5] = "wall-straight-horiz"

data[5][3] = "wall-corner-ul"
data[5][4] = "wall-corner-ur"
data[6][3] = "wall-corner-ll"
data[6][4] = "wall-corner-lr"

# C and O right
data[3][m-3] = "wall-end-r"
data[3][m-4] = "wall-straight-horiz"
data[3][m-5] = "wall-straight-horiz"
data[3][m-6] = "wall-corner-ul"
data[4][m-6] = "wall-straight-vert"
data[5][m-6] = "wall-straight-vert"
data[6][m-6] = "wall-straight-vert"
data[7][m-6] = "wall-straight-vert"
data[8][m-6] = "wall-corner-ll"
data[8][m-3] = "wall-end-r"
data[8][m-4] = "wall-straight-horiz"
data[8][m-5] = "wall-straight-horiz"

data[5][m-3] = "wall-corner-ur"
data[5][m-4] = "wall-corner-ul"
data[6][m-3] = "wall-corner-lr"
data[6][m-4] = "wall-corner-ll"



data[14][8] = "wall-end-t"
data[15][8] = "wall-straight-vert"
data[16][8] = "wall-straight-vert"
data[17][8] = "wall-end-b"

data[14][18] = "wall-end-t"
data[15][18] = "wall-straight-vert"
data[16][18] = "wall-straight-vert"
data[17][18] = "wall-end-b"



data[19][8] = "wall-corner-ul"
data[19][9] = "wall-straight-horiz"
data[19][10] = "wall-straight-horiz"
data[19][11] = "wall-corner-ur"
data[20][8] = "wall-corner-ll"
data[20][9] = "wall-straight-horiz"
data[20][10] = "wall-straight-horiz"
data[20][11] = "wall-corner-lr"



data[19][15] = "wall-corner-ul"
data[19][16] = "wall-straight-horiz"
data[19][17] = "wall-straight-horiz"
data[19][18] = "wall-corner-ur"
data[20][15] = "wall-corner-ll"
data[20][16] = "wall-straight-horiz"
data[20][17] = "wall-straight-horiz"
data[20][18] = "wall-corner-lr"


data[22][8] = "wall-end-t"
data[23][8] = "wall-straight-vert"
data[24][8] = "wall-straight-vert"
data[25][8] = "wall-end-b"


data[22][18] = "wall-end-t"
data[23][18] = "wall-straight-vert"
data[24][18] = "wall-straight-vert"
data[25][18] = "wall-end-b"


data[24][10] = "wall-corner-ul"
data[25][10] = "wall-corner-ll"
data[24][11] = "wall-corner-ur"
data[25][11] = "wall-corner-lr"


data[24][15] = "wall-corner-ul"
data[25][15] = "wall-corner-ll"
data[24][16] = "wall-corner-ur"
data[25][16] = "wall-corner-lr"


data[18][3] = "wall-end-t"
data[19][3] = "wall-straight-vert"
data[20][3] = "wall-straight-vert"
data[21][3] = "wall-straight-vert"
data[22][3] = "wall-straight-vert"
data[23][3] = "wall-straight-vert"
data[24][3] = "wall-straight-vert"
data[25][3] = "wall-end-b" 


data[18][m-3] = "wall-end-t"
data[19][m-3] = "wall-straight-vert"
data[20][m-3] = "wall-straight-vert"
data[21][m-3] = "wall-straight-vert"
data[22][m-3] = "wall-straight-vert"
data[23][m-3] = "wall-straight-vert"
data[24][m-3] = "wall-straight-vert"
data[25][m-3] = "wall-end-b" 


data[18][5] = "wall-corner-ul"
data[18][6] = "wall-corner-ur"
data[19][5] = "wall-straight-vert"
data[20][5] = "wall-straight-vert"
data[21][5] = "wall-straight-vert"
data[22][5] = "wall-straight-vert"
data[23][5] = "wall-straight-vert"
data[24][5] = "wall-straight-vert"
data[19][6] = "wall-straight-vert"
data[20][6] = "wall-straight-vert"
data[21][6] = "wall-straight-vert"
data[22][6] = "wall-straight-vert"
data[23][6] = "wall-straight-vert"
data[24][6] = "wall-straight-vert"
data[25][5] = "wall-corner-ll"
data[25][6] = "wall-corner-lr"




data[18][m-5] = "wall-corner-ur"
data[18][m-6] = "wall-corner-ul"
data[19][m-5] = "wall-straight-vert"
data[20][m-5] = "wall-straight-vert"
data[21][m-5] = "wall-straight-vert"
data[22][m-5] = "wall-straight-vert"
data[23][m-5] = "wall-straight-vert"
data[24][m-5] = "wall-straight-vert"
data[19][m-6] = "wall-straight-vert"
data[20][m-6] = "wall-straight-vert"
data[21][m-6] = "wall-straight-vert"
data[22][m-6] = "wall-straight-vert"
data[23][m-6] = "wall-straight-vert"
data[24][m-6] = "wall-straight-vert"
data[25][m-5] = "wall-corner-lr"
data[25][m-6] = "wall-corner-ll"

for i in range(n):
    data[i].append("blank")


for i in range(2 , n-1):
    for j in range(2 , m-1):
        if(data[i][j] == "blank"):
            data[i][j] = "pellet"

data[11][2] = "blank"
data[11][3] = "blank"
data[11][4] = "blank"
data[11][5] = "blank"


data[15][2] = "blank"
data[15][3] = "blank"
data[15][4] = "blank"
data[15][5] = "blank"

data[11][m-2] = "blank"
data[11][m-3] = "blank"
data[11][m-4] = "blank"
data[11][m-5] = "blank"


data[15][m-2] = "blank"
data[15][m-3] = "blank"
data[15][m-4] = "blank"
data[15][m-5] = "blank"

for i in range(11 , 16):    
    data[12][i] = "blank"
    data[13][i] = "blank"
    data[14][i] = "blank"


with open(".\\res\\levels\\1.json" , "w") as output_file:
    json.dump(data , output_file)