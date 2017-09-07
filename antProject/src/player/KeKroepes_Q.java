import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class KeKroepes_Q extends QueenBrain{
	public KeKroepes_Q(){}

	// called every an ant returns to the queen location
	public void reportingAnt(AntProperties antProperties){
		//System.out.printf("%d", antProperties.ge)
	}

	// called at the start of every turn
	public void turn(ProtectedPlayer player){
		if(player.getFood()>=5){
			player.createAnt(2, 1, 1, 90, 4, new Byte("0"));
		}

	} 
}