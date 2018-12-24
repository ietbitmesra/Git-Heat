import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

class Main{
    public static void main(String[] args) throws IOException{
        FileInputStream gridData = new FileInputStream(new File("in.txt"));
        System.setIn(gridData);
        Pacman pc = new Pacman();
        while(true){
            try{
                Thread.sleep(5);
            }
            catch(InterruptedException e){

            }
            pc.nextPosition();
        }
    }
}