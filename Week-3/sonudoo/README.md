# Git-Heat

## Running the code

1. Compile the code

    `
    javac Pacman.java Enemies.java Main.java
    `
2. Run the code

    `
    java Main
    `



## Tools Used

Language: Java 10
Dependencies: None

## Concept

Simple Graphics Techniques. 

## Customization

You can completely customize to create your own levels.
Just make the necessary changes in "in.txt" file. Check the sample for example.

1. The first line of the file contains number of rows 'n' and number of columns 'm'.
2. Then the next 'n' lines have 'm' integers each. '0' represents blocker.
3. Next line containers number of enemies 'NEY' that move in vertical direction.
4. Next 'NEY' line contains three integers each. First number represents the vertical line number. The second number represent the minimum possible position on that line and third number represents the maximum possible position on that line.
5. Next line containers number of enemies 'NEX' that move in horizontal direction.
6. Next 'NEY' line contains three integers each. First number represents the horizontal line number. The second number represent the minimum possible position on that line and third number represents the maximum possible position on that line.