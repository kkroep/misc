import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Dr_KeKroepes_Q extends QueenBrain{
	private int produced = 0;
	private AntVariant worker = new AntVariant(
		2,0,2,80,0, new Byte("0"));
	
	private AntVariant scout = new AntVariant(
		3,1,1,110,1, new Byte("0"));

	private AntVariant warrior = new AntVariant(
		5,2,0,80,2, new Byte("0"));

	public Dr_KeKroepes_Q(){
		System.out.printf("worker  %d food\n", worker.getCost());
		System.out.printf("scout   %d food\n", scout.getCost());
		System.out.printf("warrior %d food\n", warrior.getCost());

	}

	// called every an ant returns to the queen location
	public void reportingAnt(AntProperties antProperties){
		//System.out.printf("%d", antProperties.ge)
	}

	// called at the start of every turn
	public void turn(ProtectedPlayer player){
		
		if(produced<30){
			if(player.getFood()>=worker.getCost()){
				worker.createAnt(player);
				produced++;
			}
			return;
		}

		/*if(player.colonySize()<50){
			if(player.getFood()>=scout.getCost()){
				scout.createAnt(player);
				produced++;
				}
			return;
		}*/

		if(player.getFood()>=warrior.getCost()){
			warrior.createAnt(player);
			produced++;
		}
		return;








		//if(player.getFood()>=18){
			//player.createAnt(3, 3, 1, 100, 0, new Byte("0"));
		//	foodCollector.createAnt(player);
		//}

	} 
}

class AntVariant{
	private int maxHealth, damage, maxFood, maxStamina, staticMemory, cost;
	private Byte dynamicMemory;

	public AntVariant(int maxHealth, int damage, int maxFood, int maxStamina, int staticMemory, Byte dynamicMemory){
		this.maxHealth = maxHealth;
		this.damage = damage;
		this.maxFood = maxFood;
		this.maxStamina = maxStamina;
		this.staticMemory = staticMemory;
		this.dynamicMemory = dynamicMemory;

		AntProperties antProps = new AntProperties(maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);
		cost = antProps.calculateCost();
	}

	public int getCost(){return cost;}

	public boolean createAnt(ProtectedPlayer player){
		return player.createAnt(maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);
	}


}