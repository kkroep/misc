import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

// class that can be extended to form the queen brain
class QueenBrain{
	public QueenBrain(){}

	/* reportingAnt is called every time an ant reports to the queen
	 * antProperties holds the brain and properties of the ant
	 *
	 *  functions available are
	 *	antProps.getMaxHealth()
	 *  antProps.getDamage()
	 *  antProps.getMaxFood()
	 *  antProps.getMaxStamina()
	 *  antProps.calculateCost()
	 *  antProps.getDynamicMemory()
	 *  antProps.getStaticMemory()
	 *  antProps.setDynamicMemory(Byte)
	 *  antProps.setStaticMemory(Integer)
	 *
	 *  food is the amount of food the ant is carrying with him
	 *  note that the ant will eat 1 food if it can when it returns. It is hungry! 
	 */
	public void reportingAnt(AntProperties antProps, int food){
	}

	/* turn is called at the start of every turn
	 * The only things the queen can do here is decide to make a new ants and think a bit
	 *
	 * The creation of new ants requires a cost in food that is calculated like this
	 * food = 20
	 * food += (maxHealth-1)*10
	 * food += damage*10+20 
	 * cost += maxFood+20
	 * cost += maxStamina/2
	 *
	 * For ants to live they need at least
	 * maxHealth = 1;
	 * damage = 0;
	 * maxFood = 0;
	 * maxStamina = 1;
	 *
	 * when ants die they leave behind their own cost-20 worth of food 
	 */
	public void turn(ProtectedPlayer player){
	} 
}