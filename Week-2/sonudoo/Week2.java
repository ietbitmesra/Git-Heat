import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

class Week2{
	public static void main(String[] args){
		Plotter pt = new Plotter();
		String dir = "";
		try{
			dir = args[0];
		}
		catch(IndexOutOfBoundsException e){
			System.out.println("java DirectoryAnalyzer \"<folder location>\"");
			System.exit(0);
		}
		System.out.println("Counting Directories...");
		DirectoryAnalyzer.directoryArray = new Directory[DirectoryAnalyzer.countDirectories(dir)+1];
		System.out.println("Analyzing Directories...");
		DirectoryAnalyzer.buildDirectoryTree(dir, "Root", 0);
		System.out.println("Generating Plot...");
		DirectoryAnalyzer.show(pt, 1);
	}
}