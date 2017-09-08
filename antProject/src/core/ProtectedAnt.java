	// dir 	0=no direction
	//     	1=up
	//     	2=right
	//     	3=down
	//     	4=left

class ProtectedAnt{
	private Ant ant;

	public ProtectedAnt(Ant ant){
		this.ant = ant;
	}
	// not used by player
	public void setAnt(Ant ant){this.ant = ant;}


	// ------------check your own properties------------
	// when stamina runs out, the ant dies
	public int getStamina(){return ant.getStamina();}
	public int getMaxStamina(){return ant.getMaxStamina();}

	// food can be carried up to the maximum food carry capacity.
	// food is instantly given to the queen if the ant meets the queen
	public boolean hasFood(){return ant.hasFood();}
	public int getMaxFood(){return ant.getMaxFood();}
	public int getFood(){return ant.getFood();}

	// the cost of the ant is how much food the queen has to invest to produce the ant
	public int getCost(){return ant.getCost();}

	// The static and dynamic memory are the short and long term memory of type int and Byte respectively.
	// The static memory with 32 bits can only be altered by the queen
	// The dynamic memory with 8 bits can be altered by both ant and queen
	public Byte getDynamicMemory(){return ant.getDynamicMemory();}
	public int getStaticMemory(){return ant.getStaticMemory();}

	// previous direction functions as a short term spatial memory
	public int getPreviousDir(){return ant.getPreviousDir();}



	// ------------check your surroundings------------
	// how much food is there on the ground in direction? 
	public int checkFood(int dir){return ant.checkFood(dir);} 
	
	// do I smell feromones of type x of my colony in direction? fermones dissipate with a factor 0.9 each turn 
	public double getActiveFeromones(int type, int dir){return ant.getActiveFeromones(type, dir);} 
	
	// do I smell opponents in direction? The smell of a single ant dissipates with a factor 0.5 each turn
	public double getEnemyFeromones(int dir){return ant.getEnemyFeromones(dir);} 



	// ------------adjust your own properties------------
	// change the amount of feromones of type x you are releasing each turn
	public void setFeromoneDosis(double feromoneDosis){ant.setFeromoneDosis(feromoneDosis);}

	// change the single Byte of data that represents the entire short term memory of the ant
	public void setDynamicMemory(Byte value){ant.setDynamicMemory(value);}

	// you can decide to drop food you are carrying on the ground. You cannot drop more than what you are carrying with you
	public void dropFoodOnGround(int amount){ant.dropFoodOnGround(amount);}
}