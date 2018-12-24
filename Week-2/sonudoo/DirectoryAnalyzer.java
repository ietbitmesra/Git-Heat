import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

class Directory{
	int id;
	int parent;
	String name;
	String path;
	double size;
	Vector <Directory> childDirectories;
	Vector <String> childFiles;
	Vector <Double> childFilesSize;
	Directory(String name, String path, int id, int parent){
		this.id = id;
		this.parent = parent;
		this.size = 0;
		this.path = path;
		this.name = name;
		this.childDirectories = new Vector <Directory> ();
		this.childFiles = new <String> Vector();
		this.childFilesSize = new <Double> Vector();
	}
}

public class DirectoryAnalyzer{
	public static Directory[] directoryArray;
	public static int n = 1;
	public static int countDirectories(String path){
		File folder = new File(path);
		File[] listOfFiles = folder.listFiles();
		boolean containFiles = false;
		int cnt = 1;
		try{
			for(File file : listOfFiles){
				if(file.isFile() == false){
					cnt += countDirectories(path + "/" + file.getName());
				}
			}
		}
		catch(NullPointerException e){
			System.out.println("The Operating System listed a Directory that doesn't exists.");
		}
		if(containFiles == true){
			cnt += 1;
		}
		return cnt;
	}
	public static Directory buildDirectoryTree(String path, String name, int parent){
		File folder = new File(path);
		int id = DirectoryAnalyzer.n;
		DirectoryAnalyzer.directoryArray[id] = new Directory(name, path, id, parent);
		DirectoryAnalyzer.n += 1;
		double filesize = 0;
		File[] listOfFiles = folder.listFiles();
		try{
			for(File file : listOfFiles){
				if(file.isFile()){
					filesize += file.length();
					directoryArray[id].childFiles.add(file.getName());
					directoryArray[id].childFilesSize.add((double)file.length());
				}
				else{
					Directory tmp = buildDirectoryTree(path + "/" + file.getName(), file.getName(), id);
					directoryArray[id].childDirectories.add(tmp);
					directoryArray[id].size += tmp.size;
				}
			}
		}
		catch(NullPointerException e){
			System.out.println("The Operating System listed a Directory that doesn't exists.");
		}
		Directory tmp = new Directory("Current Directory Files", path + "/Files", 0 - id, id);
		tmp.size = filesize;
		directoryArray[id].childDirectories.add(tmp);
		directoryArray[id].size = directoryArray[id].size + filesize;
		return directoryArray[id];
	}
	public static void show(Plotter pt, int currentDirectoryIndex){
		Vector <String> directoryName = new <String> Vector();
		Vector <Double> directorySize = new <Double> Vector();
		LinkedHashMap <String, Double> data = new <String, Double> LinkedHashMap();
		if(currentDirectoryIndex < 0){
			// Deal with Files.
			currentDirectoryIndex = 0 - currentDirectoryIndex;
			for(int i=0;i<DirectoryAnalyzer.directoryArray[currentDirectoryIndex].childFiles.size();i++){
				String name = (String)(DirectoryAnalyzer.directoryArray[currentDirectoryIndex].childFiles.get(i));
				double size = DirectoryAnalyzer.directoryArray[currentDirectoryIndex].childFilesSize.get(i);
				directoryName.add(name);
				directorySize.add(size);
			}
			for(int i=0;i<directorySize.size();i++){
				for(int j=i+1;j<directorySize.size();j++){
					if(directorySize.get(i) < directorySize.get(j)){
						Double tmp1 = directorySize.get(i);
						directorySize.set(i, directorySize.get(j));
						directorySize.set(j, tmp1);
						String tmp2 = directoryName.get(i);
						directoryName.set(i, directoryName.get(j));
						directoryName.set(j, tmp2);
					}
				}
			}
			for(int i=0;i<directorySize.size();i++){
				data.put(directoryName.get(i), directorySize.get(i));
			}
			pt.setData(data, currentDirectoryIndex, DirectoryAnalyzer.directoryArray[currentDirectoryIndex].path+"/<File Structure>");
			pt.plot();
		}
		else if(currentDirectoryIndex > 0){
			for(int i=0;i<DirectoryAnalyzer.directoryArray[currentDirectoryIndex].childDirectories.size();i++){
				Directory tmp = (Directory)(DirectoryAnalyzer.directoryArray[currentDirectoryIndex].childDirectories.get(i));
				directoryName.add(tmp.name + "#" + Integer.toString(tmp.id));
				directorySize.add(tmp.size);
			}
			for(int i=0;i<directorySize.size();i++){
				for(int j=i+1;j<directorySize.size();j++){
					if(directorySize.get(i) < directorySize.get(j)){
						Double tmp1 = directorySize.get(i);
						directorySize.set(i, directorySize.get(j));
						directorySize.set(j, tmp1);
						String tmp2 = directoryName.get(i);
						directoryName.set(i, directoryName.get(j));
						directoryName.set(j, tmp2);
					}
				}
			}
			for(int i=0;i<directorySize.size();i++){
				data.put(directoryName.get(i), directorySize.get(i));
			}
			pt.setData(data, currentDirectoryIndex, DirectoryAnalyzer.directoryArray[currentDirectoryIndex].path);
			pt.plot();
		}
		else{
			DirectoryAnalyzer.show(pt, 1);
		}
	}
}