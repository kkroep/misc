import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Default_A extends AntBrain{

	public Default_A(){}

	public int think(ProtectedAnt ant, Random rng){

		if(ant.getDynamicMemory() == 1){
			return 5;
		}

		if(ant.getStamina()<(ant.getMaxStamina()/2+3)){
			ant.setDynamicMemory(new Byte("1"));
			return 5;
		}

		if(!ant.hasFood()){
			if(ant.checkFood(0)>0){
				ant.setDynamicMemory(new Byte("1"));
				ant.setFeromoneDosis(256/(ant.getMaxStamina()-ant.getStamina()+1));
				return 6;
			}else{
				for(int i=1; i<5; i++){
					if(ant.checkFood(i)>0)
						return i;
				}
			}
		}



		

			return (rng.nextInt(4)+1);
	}
}


