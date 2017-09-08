import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;
import java.lang.*;


class AntProperties{
	private int staticMemory = 0;
	private Byte dynamicMemory = 0; 

	private int health, maxHealth, damage, food, maxFood, stamina, maxStamina;

	public AntProperties(int maxHealth, int damage, int maxFood, int maxStamina, int staticMemory, Byte dynamicMemory){
		this.health = maxHealth;
		this.maxHealth = maxHealth;
		this.damage = damage;
		this.food = maxFood;
		this.maxFood = maxFood;
		this.stamina = maxStamina;
		this.maxStamina = maxStamina;
		this.staticMemory = staticMemory;
		this.dynamicMemory = dynamicMemory;
	}


	public void clearMemory(){
		//staticMemory = 0;
		dynamicMemory = 0; 
	}

	public void addHealth(int amount){
		health += amount;
		if(health>maxHealth)
			health = maxHealth;
	}

	public int getHealth(){return health;}
	public void replenish(){
		health = maxHealth;
		stamina = maxStamina;
	}

	public int getMaxHealth(){return maxHealth;}


	public void takeDamage(int amount){
		health -= amount;
		if(health<0)
			health = 0;
	}
	public int getDamage(){return damage;}

	public int getMaxFood(){return maxFood;}

	public int getStamina(){return stamina;}
	public int getMaxStamina(){return maxStamina;}
	public void staminaRefill(){stamina = maxStamina;}

	public int calculateCost(){
		int cost = 40;



		// health cost. starts at 4, one food for one extra
		cost += (maxHealth-1)*10;

		// damage cost
		if(damage>0)
			cost += damage*10+20; 
		
		// food cost
		if(maxFood>0)
			cost += maxFood+20; 

		cost += (int)Math.ceil((maxStamina-50)/2.0);

		// make sure the ant is a valid one
		if(maxHealth<1 || damage<0 || maxFood<0 || maxStamina<50)
			cost = Integer.MAX_VALUE;
		return cost;
	}

	public Byte getDynamicMemory(){return dynamicMemory;}
	public void setDynamicMemory(Byte value){dynamicMemory = value;}
	public int getStaticMemory(){return staticMemory;}
	public void setStaticMemory(int value){staticMemory = value;}

	public void turn(){stamina--;}
}
