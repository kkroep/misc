import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class KeKroepes_Q extends QueenBrain{
	public KeKroepes_Q(){}

	// called every an ant returns to the queen location
	public void reportingAnt(AntProperties antProps, int food){
		antProps.setDynamicMemory(new Byte("0"));
	}

	// called at the start of every turn
	public void turn(ProtectedPlayer player){
		if(player.getFood()>(160+player.colonySize()*4))
			player.createAnt(2,1,10,110, 0, new Byte("0"));
	} 
}