import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Move{
	// stand = 0
	// up = 1
	// right = 2
	// down = 3
	// left = 4
	static public int xy2dir(int x, int y){
		if(x==-1)
			return 1;
		else if(x==1)
			return 3;
		else if(y==1)
			return 2;
		else if(y==-1)
			return 4;
		else if(x!=0 || y!=0)
			System.out.printf("direction error");
		return 0;
	}

	static public int dir2x(int dir){
		if(dir==2)
			return 1;
		else if(dir==4)
			return -1;
		else
			return 0;	
	}

	static public int dir2y(int dir){
		if(dir==1)
			return -1;
		else if(dir==3)
			return 1;
		else
			return 0;	
	}

	static public int swapDir(int dir){
		if(dir == 1)
			return 3;
		else if(dir == 2)
			return 4;
		else if(dir == 3)
			return 1;
		else if(dir == 4)
			return 2;
		else
			return 0;
	}
}
