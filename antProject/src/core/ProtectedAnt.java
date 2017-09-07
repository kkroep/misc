class ProtectedAnt{
	private Ant ant;

	public ProtectedAnt(Ant ant){
		this.ant = ant;
	}

	public void setAnt(Ant ant){this.ant = ant;}
	public int getStamina(){return ant.getStamina();}
	public int getMaxStamina(){return ant.getMaxStamina();}
	public boolean hasFood(){return ant.hasFood();}
	public int getFood(){return ant.getFood();}
	public int getMaxFood(){return ant.getMaxFood();}
	public int checkFood(int dir){return ant.checkFood(dir);}
	//public void gatherFood(){ant.gatherFood();}
	public double getActiveFeromones(int type, int dir){return ant.getActiveFeromones(type, dir);}
	public double getEnemyFeromones(int dir){return ant.getEnemyFeromones(dir);}
	public void setFeromoneDosis(double feromoneDosis){ant.setFeromoneDosis(feromoneDosis);}
	public int getPreviousDir(){return ant.getPreviousDir();}
	public Byte getDynamicMemory(){return ant.getDynamicMemory();}
	public int getStaticMemory(){return ant.getStaticMemory();}
	public void setDynamicMemory(Byte value){ant.setDynamicMemory(value);}
	public void clearMemory(){ant.clearMemory();}
}