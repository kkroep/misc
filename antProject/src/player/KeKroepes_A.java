import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class KeKroepes_A extends AntBrain{

	public KeKroepes_A(){}

	public int think(ProtectedAnt ant, Random rng){
		/////////// PLAYER ADDED FUNCTIONAILTY

		// calculate incentives
		double inc[] = {1,1,1,1,1};
		int dir = 0;	


		// return if almost out of juice
		if(ant.getStamina()<(ant.getMaxStamina()/2+1)){
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

		if(ant.getDynamicMemory() == 1){
			return 5;
		}

		// border protection
		/*if(x==0)
			inc[4]=0;
		if(x==63)
			inc[2]=0;
		if(y==0)
			inc[1]=0;
		if(y==63)
			inc[3]=0;
		*/	
		// penalty for staying stationary
		inc[0] *= 0.02;

		
		// add value of feromones
		for(int i=1; i<5; i++){
			if(inc[i]!=0)
				inc[i] += ant.getActiveFeromones(0,i);
		}

		
		if(ant.getStamina()<ant.getMaxStamina()){
			// incentive for moving forward
			inc[ant.getPreviousDir()] *= 4;

			// penalty for going back
			inc[Move.swapDir(ant.getPreviousDir())] *= 0.02;
		}

		
		// when incentives are generated pick a probabilistic random one
		double tmp = (inc[0]+inc[1]+inc[2]+inc[3]+inc[4])*rng.nextDouble();
		for(int i=0; i<5; i++){
			tmp -=inc[i];
			if(tmp<=0){
				dir = i;
				break;
			}
		}
		

		// dir now stores the new direction. Update everything
		return dir;
		}
}


