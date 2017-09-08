import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Referee{
	private int w,h;
	private int[][] food = new int[128][128];
	private Random rng = new Random();
	private ArrayList<PlayerGrid> grid = new ArrayList<PlayerGrid>();
	private int playerCount;
	private int foodConcentration = 400;


	public Referee(int foodAmount, int w, int h, int playerCount){
		this.w = w;
		this.h = h;
		this.playerCount = playerCount;

		//rng.setSeed(0);
		for(int i=0; i<playerCount; i++)
			grid.add(new PlayerGrid());

		int x,y;
		for(int i=0; i<foodAmount; i++){
			x = rng.nextInt(w/2);
			y = rng.nextInt(h/2);
			food[x][y] += foodConcentration;
			food[128-1-y][x] += foodConcentration;
			food[y][128-1-x] += foodConcentration;
			food[128-1-x][128-1-y] += foodConcentration;
		}
	}

	public void addFood(int x, int y, int amount){
		food[x][y] += amount;
	}

	public void addActiveFeromones(int x, int y, int playerNumber, double dosis){
		grid.get(playerNumber).addActiveFeromones(x, y, 0, dosis);
	}

	public void addEnemyFeromones(int x, int y, int playerNumber){
		for(int j=0; j<playerCount; j++){
			if(j!=playerNumber){
				grid.get(j).addEnemyFeromones(x, y, 1);
			}
		}
	}

	public int takeDamage(int x, int y, int playerNumber, int health){ 
		return grid.get(playerNumber).takeDamage(x, y, health);
	}

	public void addCoreDamage(int x, int y, int playerNumber, int amount){
		for(int j=0; j<playerCount; j++){
			if(j!=playerNumber){
				grid.get(j).addDamage(x, y, amount);
			}
		}
	}

	public void addplashDamage(int x, int y, int playerNumber, int amount){
		for(int i=1; i<5; i++){
			for(int j=0; j<playerCount; j++){
				if(j!=playerNumber)
					grid.get(j).addDamage(x+Move.dir2x(i), y+Move.dir2y(i), amount);
			}
		}
	}

	public double getActiveFeromones(int x, int y, int playerNumber, int type){
		return grid.get(playerNumber).getActiveFeromones(x,y,type);
	}

	public double getEnemyFeromones(int x, int y, int playerNumber){
		return grid.get(playerNumber).getEnemyFeromones(x,y);
	}

	public int gatherFood(int x, int y, int capacity){
		//System.out.printf("%d", capacity);
		int gatheredFood = 0;
		if(capacity>food[x][y]){
			gatheredFood = food[x][y];
			food[x][y] = 0;
		}
		else{
			food[x][y] -= capacity;
			gatheredFood = capacity;
		}

		return gatheredFood;
	}


	public int checkFood(int x, int y){	return food[x][y];}

	public void draw(int[][][] picture){
		//ig2.setPaint(Color.green);
		for(int i=0; i<128; i++){
			for(int j=0; j<128; j++){
				if(food[i][j]>200){
					picture[i][j][0]+=100;
				    picture[i][j][1]+=100;
				    picture[i][j][2]+=100;
				}
				else{
					picture[i][j][0]+=(food[i][j]>>1);
				    picture[i][j][1]+=(food[i][j]>>1);
				    picture[i][j][2]+=(food[i][j]>>1);
				}
			}
		}
	}

	public void turn(){
		for(int i=0; i<grid.size(); i++)
			grid.get(i).turn(0.9);
	}
}



class PlayerGrid{
	private double[][][] activeFeromones = new double[128][128][4];
	private double[][] enemyFeromones = new double[128][128];
	private int[][] damageGrid = new int[128][128];

	public PlayerGrid(){
		for(int i=0; i<128; i++)
			for(int j=0; j<128; j++)
			{
				enemyFeromones[i][j] = 0;
				for(int k=0; k<4; k++)
					activeFeromones[i][j][k] = 0;
			}
	}

	public void addActiveFeromones(int x, int y, int type, double dosis){	activeFeromones[x][y][type] += dosis;}
	public void addEnemyFeromones(int x, int y, double dosis){	enemyFeromones[x][y] += dosis;}
	public void addDamage(int x, int y, int amount){damageGrid[x][y] += amount;}


	public double getActiveFeromones(int x, int y, int type){return activeFeromones[x][y][type];}
	public double getEnemyFeromones(int x, int y){return enemyFeromones[x][y];}
	//public int checkDamage(int x, int y){return damageGrid[x][y];}

	public int takeDamage(int x, int y, int health){
		if(damageGrid[x][y]>8)
			damageGrid[x][y]=8;

		if(health<damageGrid[x][y])
		{
			damageGrid[x][y] -= health;
			return health;
		}
		else
		{
			int damage = damageGrid[x][y];
			damageGrid[x][y] = 0;
			return damage;
		}
	}


	public void turn(double decay){
		for(int i=0; i<128; i++)
			for(int j=0; j<128; j++)
			{
				damageGrid[i][j] = 0;
				enemyFeromones[i][j] *= 0.7;
				for(int k=0; k<4; k++)
					activeFeromones[i][j][k] *= decay;
			}
	}
}




