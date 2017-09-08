import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class AntBrain{
	public AntBrain(){}

	/* think is called every step by every ant. The player should extend this class and alter this function
	 *
	 * This function can return 8 meaningfull actions
	 * 0 = idle
	 * 1 = go up
	 * 2 = go right
	 * 3 = go down
	 * 4 = go left
	 * 5 = go one step reverse
	 * 6 = gather food on location
	 * 7 = eat food on location and replenish 4 health and all stamina consuming 1 food on ground
	 *
	 * The ant automatically attacks enemy ants that share the same position as him
	 */ 
	public int think(ProtectedAnt ant, Random rng){
		return 0;
	}
}


