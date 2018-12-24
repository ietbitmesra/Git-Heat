import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

class Enemies{
    int direction;
    int minPos;
    int maxPos;
    int currentPos;
    int line;
    int currentDirection;
    Enemies(int direction, int minPos, int maxPos, int line){
        this.direction = direction;
        this.minPos = minPos;
        this.maxPos = maxPos;
        this.line = line;
        this.currentPos = (int)(Math.random()*(maxPos-minPos)) + minPos;
        if((Math.random()*19803) % 2 == 0)
            this.currentDirection = 1;
        else
            this.currentDirection = 0;
    }
}