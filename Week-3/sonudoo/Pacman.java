import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

class Pacman extends JPanel implements KeyListener{
    JFrame mainFrame;
    int[][] gridData;
    int[][] isMarked;
    int posX;
    int posY;
    int maxX;
    int maxY;
    int dir;
    int totalPoints;
    int score;
    int n;
    int m;
    Enemies enemyX[];
    Enemies enemyY[];
    int enemyXn;
    int enemyYn;
    Pacman(){
        mainFrame = new JFrame("Pacman");
        mainFrame.add(this);
        mainFrame.setResizable(false);
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Scanner inputScanner = new Scanner(System.in);
        n = inputScanner.nextInt();
        m = inputScanner.nextInt();
        mainFrame.setSize((m+1)*20, (n+2)*20);
        gridData = new int[n][m];
        isMarked = new int[n][m];
        totalPoints = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                gridData[i][j] = inputScanner.nextInt();
                if(gridData[i][j] == 1){
                    totalPoints++;
                }
                isMarked[i][j] = 0;
            }
        }
        enemyXn = inputScanner.nextInt();
        enemyX = new Enemies[enemyXn];
        for(int i=0;i<enemyXn;i++){
            int gridNumber = inputScanner.nextInt(), minPos = inputScanner.nextInt(), maxPos = inputScanner.nextInt();
            enemyX[i] = new Enemies(0, (minPos-1)*20 + 10, (maxPos-1)*20 + 10, (gridNumber-1)*20 + 10);
        }
        enemyYn = inputScanner.nextInt();
        enemyY = new Enemies[enemyYn];
        for(int i=0;i<enemyYn;i++){
            int gridNumber = inputScanner.nextInt(), minPos = inputScanner.nextInt(), maxPos = inputScanner.nextInt();
            enemyY[i] = new Enemies(1, (minPos-1)*20 + 10, (maxPos-1)*20 + 10, (gridNumber-1)*20 + 10);
        } 
        posX = 0;
        posY = 0;
        dir = -1;
        maxX = 0;
        maxY = 0;
        score = 0;
        mainFrame.addKeyListener(this);
        repaint();
        mainFrame.setVisible(true);
    }
    public void paint(Graphics currentGraphics){
        int currrentX = 0;
        int currrentY = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(gridData[i][j] == 1){
                    currentGraphics.setColor(Color.black);
                    currentGraphics.fillRect(currrentX, currrentY, 20, 20);
                    if(isMarked[i][j] == 0){
                        currentGraphics.setColor(Color.yellow);
                        currentGraphics.fillOval(currrentX+8, currrentY+8, 4, 4);
                    }
                }
                else{
                    currentGraphics.setColor(Color.white);
                    currentGraphics.fillRect(currrentX, currrentY, 20, 20);
                }
                maxX = Math.max(maxX, currrentX);
                maxY = Math.max(maxY, currrentY);
                currrentX += 20;
            }
            currentGraphics.setColor(Color.yellow);
            currentGraphics.fillArc(posX, posY, 20, 20, 0, 360);
            currrentX = 0;
            currrentY += 20;
        }
        currentGraphics.setColor(Color.blue);
        for(int i=0;i<enemyXn;i++){
            currentGraphics.fillOval(enemyX[i].line - 10, enemyX[i].currentPos - 10, 20, 20);
        }
        for(int i=0;i<enemyYn;i++){
            currentGraphics.fillOval(enemyY[i].currentPos - 10, enemyY[i].line - 10, 20, 20);
        }
    }
    public void nextPosition(){
        int newPosX = posX, newPosY = posY;
        if(dir == 0){
            newPosX = posX - 1;
            newPosY = posY;
        }
        else if(dir == 1){
            newPosX = posX;
            newPosY = posY - 1;
        }
        else if(dir == 2){
            newPosX = posX + 1;
            newPosY = posY;
        }
        else if(dir == 3){
            newPosX = posX;
            newPosY = posY + 1;
        }
        if(newPosX >= 0 && newPosY >= 0 && newPosX <= maxX && newPosY <= maxY){
            try{
                int boxX1 = (newPosX+20)/20;
                int boxY1 = (newPosY+20)/20;
                int boxX2 = (newPosX)/20;
                int boxY2 = (newPosY)/20;
                int boxX3 = (newPosX+20)/20;
                int boxY3 = (newPosY)/20;
                int boxX4 = (newPosX)/20;
                int boxY4 = (newPosY+20)/20;

                if(gridData[boxY1][boxX1] == 1 && gridData[boxY2][boxX2] == 1 && 
                    gridData[boxY3][boxX3] == 1 && gridData[boxY4][boxX4] == 1){
                    posX = newPosX;
                    posY = newPosY;
                }
            }
            catch(IndexOutOfBoundsException e){

            }
        }
        int centerX = posX + 10;
        int centerY = posY + 10;
        int currrentX = 0;
        int currrentY = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                int currentDotCenterX = currrentX + 10;
                int currentDotCenterY = currrentY + 10;
                int dist = (int)Math.sqrt((currentDotCenterX - centerX)*(currentDotCenterX - centerX) 
                                        + (currentDotCenterY - centerY)*(currentDotCenterY - centerY));
                if(dist <= 10){
                    if(isMarked[i][j] == 0){
                        isMarked[i][j] = 1;
                        score++;
                        if(score == totalPoints){
                            System.out.println("You Won!");
                        }
                    }
                }
                currrentX += 20;
            }
            currrentX = 0;
            currrentY += 20;
        }
        for(int i=0;i<enemyXn;i++){
            if(enemyX[i].currentDirection == 1){
                if(enemyX[i].currentPos + 1 > enemyX[i].maxPos){
                    enemyX[i].currentPos -= 1;
                    enemyX[i].currentDirection = 0;
                }
                else{
                    enemyX[i].currentPos += 1;
                }
            }
            else{
                if(enemyX[i].currentPos - 1 < enemyX[i].minPos){
                    enemyX[i].currentPos += 1;
                    enemyX[i].currentDirection = 1;
                }
                else{
                    enemyX[i].currentPos -= 1;
                }   
            }
            int dist = (int)Math.sqrt((enemyX[i].line - centerX)*(enemyX[i].line - centerX) 
                            + (enemyX[i].currentPos - centerY)*(enemyX[i].currentPos - centerY));
            if(dist < 19){
                System.out.println("Game Over!");
                System.exit(0);
            }
        }
        for(int i=0;i<enemyYn;i++){
            if(enemyY[i].currentDirection == 1){
                if(enemyY[i].currentPos + 1 > enemyY[i].maxPos){
                    enemyY[i].currentPos -= 1;
                    enemyY[i].currentDirection = 0;
                }
                else{
                    enemyY[i].currentPos += 1;
                }
            }
            else{
                if(enemyY[i].currentPos - 1 < enemyY[i].minPos){
                    enemyY[i].currentPos += 1;
                    enemyY[i].currentDirection = 1;
                }
                else{
                    enemyY[i].currentPos -= 1;
                }   
            }
            int dist = (int)Math.sqrt((enemyY[i].currentPos - centerX)*(enemyY[i].currentPos - centerX) 
                            + (enemyY[i].line - centerY)*(enemyY[i].line - centerY));
            if(dist < 19){
                System.out.println("Game Over!");
                System.exit(0);
            }
        }
        repaint();
    }
    public void keyPressed(KeyEvent e) {  
        if(e.getKeyCode() == KeyEvent.VK_LEFT)    dir = 0;
        else if(e.getKeyCode() == KeyEvent.VK_UP)   dir = 1;
        else if(e.getKeyCode() == KeyEvent.VK_RIGHT)   dir = 2;
        else if(e.getKeyCode() == KeyEvent.VK_DOWN)   dir = 3;  
    }  
    public void keyReleased(KeyEvent e){ 
    }  
    public void keyTyped(KeyEvent e){   
    }  
}
