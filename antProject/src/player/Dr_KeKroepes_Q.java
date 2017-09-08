import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Dr_KeKroepes_Q extends QueenBrain{
	private int produced = 0, frame = 0, foodEfficiency = 100;
	private AntVariant worker = new AntVariant(
		1,0,1,50, new Byte("0"));
	
	private AntVariant scout = new AntVariant(
		1,0,0,110, new Byte("0"));

	private AntVariant warrior = new AntVariant(
		5,2,0,90, new Byte("0"));

	private AntVariant standard = new AntVariant(
		2, 1, 1, 90, new Byte("0"));

	private int forcedDir = 0;

	public Dr_KeKroepes_Q(){
		System.out.printf("worker  %d food\n", worker.getCost());
		System.out.printf("scout   %d food\n", scout.getCost());
		System.out.printf("warrior %d food\n", warrior.getCost());
		System.out.printf("standard %d food\n", standard.getCost());

	}

	// called every an ant returns to the queen location
	public void reportingAnt(AntProperties antProps, int food){
		//System.out.printf(".");
		//if(antProps.getStaticMemory()==4)
			//System.out.printf("W");


		antProps.setDynamicMemory(new Byte("0"));
		int staticMemory = antProps.getStaticMemory();
		staticMemory = staticMemory & 15;
		staticMemory += forcedDir<<4;
		//System.out.printf("(%d)", staticMemory);
		antProps.setStaticMemory(staticMemory);

		if(food>0)
			foodEfficiency += 6;
		else
			foodEfficiency--;

		//System.out.printf("%d", antProperties.ge)
	}

	// called at the start of every turn
	public void turn(ProtectedPlayer player){
		frame++;
		int type = 0; 

        if(frame%250==0)
        	System.out.printf("(%d)", foodEfficiency);


		if(frame<2000)
			foodEfficiency = 10;

		if(frame==2000)
			foodEfficiency = 0;

		if(foodEfficiency>100)
			foodEfficiency = 100;

		if( foodEfficiency <= 0){
			System.out.printf("\nF:%d ---SWITCH! ", frame);
			foodEfficiency = 100;
			if(forcedDir==0)
				forcedDir = 4;
			else if(forcedDir == 4)
				forcedDir = 1;
			else
				forcedDir++;
		}

		/*if(frame<2500){
			forcedDir = 0;	
		}if(frame>2500){
			forcedDir = 1;
		}if(frame>4000){
			forcedDir = 4;
		}if(frame>5500){
			forcedDir = 2;
		}*/

		/*if(frame>3500){
			forcedDir = 2;
		}
		if(frame>9000){
			forcedDir = 3;
		}*/

		int staticMemory = 0;
		staticMemory += (forcedDir<<4);


		switch (type){
			case 0: if(player.getFood()>=standard.getCost()){
								if(standard.createAnt(player, staticMemory+0)){
									produced++;
								}else{
									System.out.printf("Err:%d ", player.getFood());
								}
							 }
							 break;
			default: 		if(player.getFood()>=standard.getCost()){
								standard.createAnt(player, staticMemory+0);
								produced++;
							 }
							 break;
		}

		/*if(player.colonySize()<50){
			if(player.getFood()>=scout.getCost()){
				scout.createAnt(player);
				produced++;
				}
			return;
		}

		if(player.getFood()>=warrior.getCost()){
			warrior.createAnt(player);
			produced++;
		}*/
		return;
	} 
}

class AntVariant{
	private int maxHealth, damage, maxFood, maxStamina, staticMemory, cost;
	private Byte dynamicMemory;

	public AntVariant(int maxHealth, int damage, int maxFood, int maxStamina, Byte dynamicMemory){
		this.maxHealth = maxHealth;
		this.damage = damage;
		this.maxFood = maxFood;
		this.maxStamina = maxStamina;
		this.dynamicMemory = dynamicMemory;

		AntProperties antProps = new AntProperties(maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);
		cost = antProps.calculateCost();
	}

	public int getCost(){return cost;}

	public boolean createAnt(ProtectedPlayer player, int staticMemory){
		return player.createAnt(maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);
	}


}