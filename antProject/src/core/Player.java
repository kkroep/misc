import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;
import java.lang.reflect.Constructor;


class Player{
	private int x;
	private int y;
	private int food;
	private int[] color;
	private int playerNumber;
	private ArrayList<Ant> ants;
	private ProtectedPlayer protectedPlayer = new ProtectedPlayer(this);
	private QueenBrain queenBrain = new QueenBrain();
	private Referee referee;
	private Constructor antBrainCtor;
	private String playerName;

	public Player(int[] color, int playerNumber, int x, int y, int food, Referee referee, String playerName) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.food = food;
		this.referee = referee;
		this.playerNumber = playerNumber;
		this.ants = new ArrayList<Ant>();
		this.playerName = playerName;

	
		// based on the player name, find the queen and ant brains	
	    try
	    {
	    	// antbrain part
	        AntBrain antBrain = (AntBrain)Class.forName(String.format("%s_A", playerName)).newInstance();
	        Class<? extends AntBrain> c = antBrain.getClass();
	        antBrainCtor = c.getConstructor();

	        // queen brain part
	        queenBrain = (QueenBrain)Class.forName(String.format("%s_Q", playerName)).newInstance();
	    }
	    catch(Exception e1)
	    {
	        System.out.printf("Invalid antbrain or queenBrain for %s\n", playerName);

	        // try to give it the default AI
	        try
		    {
		    	// antbrain part
		        AntBrain antBrain = (AntBrain)Class.forName(String.format("Default_A")).newInstance();
		        Class<? extends AntBrain> c = antBrain.getClass();
		        antBrainCtor = c.getConstructor();

		        // queen brain part
		        queenBrain = (QueenBrain)Class.forName(String.format("Default_Q")).newInstance();
		    }
		    catch(Exception e2)
		    {
		        System.out.printf("\n\nEXCEPTION: simulation is compromised. No default colony brain in place!\n\n");
		    }
		    }
	}

	// set functions
	//public void setX(int x){this.x = x;}
	//public void setY(int y){this.y = y;}
	//public void setPlayerNumber(int playerNumber){this.playerNumber = playerNumber;}

	// get functions
	public int getX(){return x;}
	public int getY(){return y;}
	public int[] getColor(){return color;}
	public int getFood(){return food;}
	public int getPlayerNumber(){return playerNumber;}
	public String getName(){return playerName;}


	// draw everything of this playuer on the board
	public void draw(int[][][] picture){
		//ig2.setPaint(Color.blue);

	    Iterator<Ant> iterator = ants.iterator();
		while (iterator.hasNext()){
			iterator.next().draw(picture, color);
		}
		//ig2.setPaint(Color.red);
	    //ig2.fill(new Rectangle2D.Double(x*8, y*8, 8, 8));
	    picture[x][y][0]+=color[0];
	    picture[x][y][1]+=color[1];
	    picture[x][y][2]+=color[2];
	}

	public int colonySize(){
		return ants.size();
	}

	public int colonyFood(){
		int totalFood = food;

		Iterator<Ant> iterator = ants.iterator();
		while (iterator.hasNext()){
			Ant ant = iterator.next();
			totalFood += ant.getCost();
		}
		return totalFood;
	}

	public void reportingAnt(AntProperties antProperties, int food){
		queenBrain.reportingAnt(antProperties, food);
	}

	public boolean createAnt(int maxHealth, int damage, int maxFood, int maxStamina, int staticMemory, Byte dynamicMemory){
			try
			{
				Ant ant = new Ant(x,y, referee, (AntBrain)antBrainCtor.newInstance(), playerNumber, maxHealth, damage, maxFood, maxStamina, staticMemory, dynamicMemory);
				//ants.add(new Ant(x,y, referee, (AntBrain)antBrainCtor.newInstance(), playerNumber, 3, 1, 1, 100)); 
				int cost = ant.getCost();
				
				if(food>=cost){
					ants.add(ant);
					food -= cost;
					return true;
				}
				return false;
			}
			catch(Exception e){
				System.out.printf("EXCEPTION: failed to make ant\n");
				return false;
			}
	}

	public void takeDamage(){
		Iterator<Ant> iterator = ants.iterator();
		while (iterator.hasNext()){
			Ant ant = iterator.next();

			ant.takeDamage();

			// check of ant has returned and if so how much food
			if(ant.isDead())
			{
				referee.addFood(ant.getX(), ant.getY(), ant.getCost());
				iterator.remove();
			}
		}
	}

	// execute a turn
	public final void turn(){
		queenBrain.turn(protectedPlayer);


		// turn for the ants
		Iterator<Ant> iterator = ants.iterator();
		while (iterator.hasNext()){
			Ant ant = iterator.next();

			// do asnt loop
			int action = ant.turn();
			if(action==6)
				ant.gatherFood();
			else
				ant.move(action);

			// check of ant has returned and if so how much food
			//if(ant.isDead())
			//{
				//referee.addFood(ant.getX(), ant.getY(), 5);
				//iterator.remove();
			//}
			ant.applyAnt2Grid();
			if(ant.endTurn(x, y)){
				queenBrain.reportingAnt(ant.getAntProps(), food);
				food += ant.dropFood();
			}
		}

		//System.out.printf("a= %d\n", ants.size());
	}
}


