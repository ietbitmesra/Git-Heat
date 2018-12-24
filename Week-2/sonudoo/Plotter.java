import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

public class Plotter extends JPanel implements MouseListener{
	JFrame mainFrame;
	LinkedHashMap <String, Double> dir; 
	double sum;
	int n;
	int marked;
	boolean filesOnly;
	int currentDirectoryIndex;
	String currentDirectory;
	double startAngle[];
	double endAngle[];
	String name[];
	double size[];
	int id[];
	Color[] c;
	Plotter(){
		this.marked = -1;
		this.filesOnly = false;
		this.mainFrame = new JFrame("Directory Structure");
		mainFrame.add(this);
		mainFrame.setSize(1000, 600);
		mainFrame.setResizable(false);
		mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		addMouseListener(this);
	}
	public void setData(LinkedHashMap <String, Double> dir, int currentDirectoryIndex, String currentDirectory){
		this.currentDirectory = currentDirectory;
		this.currentDirectoryIndex = currentDirectoryIndex;
		this.filesOnly = false;
		this.dir = dir;
		this.sum = 0;
		this.n = 0;
		for(Map.Entry m : dir.entrySet()){  
			this.sum += (double)m.getValue();
			this.n += 1;
		}  
		this.c = new Color[this.n];
		this.startAngle = new double[this.n];
		this.endAngle = new double[this.n];
		this.name = new String[this.n];
		this.size = new double[this.n];
		this.id = new int[this.n];
		double angle = 0;
		int i = 0;
		for(Map.Entry m : dir.entrySet()){
			this.c[i] = Color.getHSBColor((360.0f - (360.0f/this.n)*i)/360.0f, 0.7f, 0.8f);
			double requiredAngle = ((double)m.getValue()/this.sum)*360;
			this.startAngle[i] = angle;
			this.endAngle[i] = angle + requiredAngle;
			angle += requiredAngle;
			this.name[i] = (String)m.getKey();
			try{
				String s[] = this.name[i].split("#");
				this.name[i] = s[0];
				this.id[i] = Integer.parseInt(s[1]);
			}
			catch(IndexOutOfBoundsException e){
				this.filesOnly = true;
			}
			this.size[i] = (double)m.getValue();
			i++;
		}
	}
	public void paint(Graphics currentGraphics){
		this.marked = -1;
		currentGraphics.setColor(new Color(255, 255, 255));
		currentGraphics.fillRect(0, 0, 1000, 600);
		boolean others = false;
		currentGraphics.setColor(Color.black);
		currentGraphics.drawString("Present Working Directory: "+currentDirectory, 50, 25);
		for(int i=0;i<this.n;i++){
			currentGraphics.setColor(this.c[i]);
			currentGraphics.fillArc(100, 100, 400, 400, (int)this.startAngle[i], 
										(int)(this.endAngle[i] - this.startAngle[i]));
			if((int)(this.endAngle[i] - this.startAngle[i]) > 1){
				currentGraphics.fillRect(600, 100 + i*30, 20, 20);
				currentGraphics.setColor(Color.black);
				currentGraphics.drawString(this.name[i] + " - " + 
										Integer.toString((int)((this.endAngle[i]-this.startAngle[i])/3.6f)) + "%", 630, 115 + i*30); 
			}
			else if(others == false){
				currentGraphics.setColor(this.c[this.n-1]);
				currentGraphics.fillRect(600, 100 + i*30, 20, 20);
				currentGraphics.setColor(Color.black);
				currentGraphics.drawString("Others "+(this.n-i-1)+" File(s)/Folders(s) - < 1%", 630, 115 + i*30); 
				others = true;
			}
		}
		currentGraphics.setColor(Color.gray);
		currentGraphics.fillRect(50, 50, 40, 20);
		currentGraphics.setColor(Color.black);
		currentGraphics.drawString("Back", 55, 60); 
	}
	public void plot(){
		mainFrame.setVisible(false);
		repaint();
		mainFrame.setVisible(true);
	}
	
	public void mouseClicked(MouseEvent e){
		double r = Math.sqrt((e.getX()-300)*(e.getX()-300) + (e.getY()-300)*(e.getY()-300));  
  		if(r <= 200){
  			double cosineInverse = Math.toDegrees(Math.acos((e.getX()-300)/r));
  			double tangentInverse = Math.toDegrees(Math.atan((300-e.getY())/(1.0*(e.getX()-300))));
  			double angle = -1;
  			if(cosineInverse <= 90 && tangentInverse >= 0){
  				angle = tangentInverse;
  			}
  			else if(cosineInverse > 90 && tangentInverse < 0){
  				angle = cosineInverse;
  			}
  			else if(cosineInverse > 90 && tangentInverse > 0){
  				angle = (360 - cosineInverse);
  			}
  			else{
  				angle = (360 - cosineInverse);
  			}
  			int low = 0;
  			int high = this.n - 1;
  			while(low<=high){
  				int mid = (low+high)>>1;
  				if(startAngle[mid]<=angle && angle<=endAngle[mid]){
  					break;
  				}
  				else if(startAngle[mid] > angle){
  					high = mid - 1;
  				}
  				else{
  					low = mid + 1;
  				}
  			}
  			Graphics currentGraphics = this.getGraphics();
	  		if(this.marked != -1){
	  			currentGraphics.setColor(Color.white);
	  			currentGraphics.fillArc(80, 80, 440, 440, (int)this.startAngle[this.marked], 
	  									(int)(this.endAngle[this.marked] - this.startAngle[this.marked]));
	  			currentGraphics.setColor(c[this.marked]);
	  			currentGraphics.fillArc(100, 100, 400, 400, (int)this.startAngle[this.marked],
	  									(int)(this.endAngle[this.marked] - this.startAngle[this.marked]));
	  		}
  			if(e.getClickCount() >= 2 && this.filesOnly == false){
	  			int mid = (low+high)>>1;
				DirectoryAnalyzer.show(this, this.id[mid]);
			}
			else{
	  			this.marked = (low+high)>>1;
	  			currentGraphics.setColor(c[this.marked]);
	  			currentGraphics.fillArc(80, 80, 440, 440, (int)this.startAngle[this.marked],
	  									(int)(this.endAngle[this.marked] - this.startAngle[this.marked]));
	  		}
  		}
  		else if(e.getX()>=50 && e.getX() <= 90 && e.getY()>=50 && e.getY()<=70){
  			if(this.filesOnly == true)
  				DirectoryAnalyzer.show(this, currentDirectoryIndex);
  			else
  				DirectoryAnalyzer.show(this, DirectoryAnalyzer.directoryArray[currentDirectoryIndex].parent);
  		}
  		else{
  			Graphics currentGraphics = this.getGraphics();
  			if(this.marked != -1){
  				currentGraphics.setColor(Color.white);
  				currentGraphics.fillArc(80, 80, 440, 440, (int)this.startAngle[this.marked],
  										(int)(this.endAngle[this.marked] - this.startAngle[this.marked]));
  				currentGraphics.setColor(c[this.marked]);
  				currentGraphics.fillArc(100, 100, 400, 400, (int)this.startAngle[this.marked],
  										(int)(this.endAngle[this.marked] - this.startAngle[this.marked]));
  			}
  			marked = -1;
  		}
	}  
	public void mouseEntered(MouseEvent e){ 
	}  
	public void mouseExited(MouseEvent e){  
	}  
	public void mousePressed(MouseEvent e){  
	}  
	public void mouseReleased(MouseEvent e){  
	} 
}

