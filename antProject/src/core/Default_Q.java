import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Default_Q extends QueenBrain{
	public Default_Q(){}

	// called every an ant returns to the queen location
	public void reportingAnt(AntProperties antProps, int food){
		antProps.setDynamicMemory(new Byte("0")); // make sure the ant stops returning
	}

	// called at the start of every turn
	public void turn(ProtectedPlayer player){
		if(player.getFood()>=250){ // some food must be leftover for the returning ants to eat
			player.createAnt(2, 1, 1, 100, 0, new Byte("0"));
		}

	} 
}