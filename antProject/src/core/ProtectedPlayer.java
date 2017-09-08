import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class ProtectedPlayer{
	private Player player;

	public ProtectedPlayer(Player player){
		this.player = player;
	}

	// The amount of ants that are currently alive in the colony
	public int colonySize(){return player.colonySize();}
	
	// returns true if succesfull with creating an ant and false if not. It wont create an ant if it doesn't have the food required for it
	public boolean createAnt(int maxHealth, int damage, int maxFood, int maxStamina, int staticMemory, Byte dynamicMemory){return player.createAnt(maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);}
	
	// the amount of food that the queen currently has at its disposal
	public int getFood(){return player.getFood();}
}





