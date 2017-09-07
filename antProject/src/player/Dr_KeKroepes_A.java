import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.geom.Rectangle2D;
import java.util.*;

class Dr_KeKroepes_A extends AntBrain{

	public Dr_KeKroepes_A(){}

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

		if(ant.getFood()<ant.getMaxFood()){
			if(ant.checkFood(0)>0){
				ant.setDynamicMemory(new Byte("1"));
				ant.setFeromoneDosis(ant.checkFood(0)*10/(ant.getMaxStamina()-ant.getStamina()+1));
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

		//for worker
		if(ant.getStaticMemory()==0){
			for(int i=1; i<5; i++){
				if(ant.getEnemyFeromones(i)>0.2){
					ant.setDynamicMemory(new Byte("1"));
					System.out.printf("H");
					return 5;
					}
				if(inc[i]!=0){
					inc[i] += ant.getActiveFeromones(0,i);
				}
			}
		}

		// for scout do nothing, litterally :P
		if(ant.getStaticMemory()==1){
			for(int i=1; i<5; i++){
				if(inc[i]!=0){
					inc[i] += ant.getActiveFeromones(0,i)/2;
				}
			}
		}


		//for warrior
		if(ant.getStaticMemory()==2){
			for(int i=1; i<5; i++){
				if(inc[i]!=0){
					inc[i] += ant.getActiveFeromones(0,i);
					//inc[i] += ant.getEnemyFeromones(i);
				}
			}
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

		private int worker(ProtectedAnt ant, Random rng){
		/////////// PLAYER ADDED FUNCTIONAILTY

		// calculate incentives
		double inc[] = {1,1,1,1,1};
		int dir = 0;	


		// return if almost out of juice
		if(ant.getStamina()<(ant.getMaxStamina()/2+1)){
			ant.setDynamicMemory(new Byte("1"));
			return 5;
		}

		if(ant.getFood()<ant.getMaxFood()){
			if(ant.checkFood(0)>0){
				ant.setDynamicMemory(new Byte("1"));
				ant.setFeromoneDosis(ant.checkFood(0)*10/(ant.getMaxStamina()-ant.getStamina()+1));
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

		// penalty for staying stationary
		inc[0] *= 0.1;

		
		// add value of feromones

		//for worker
		for(int i=1; i<5; i++){
			/*if(ant.getEnemyFeromones(i)>0.2){
				ant.setDynamicMemory(new Byte("1"));
				System.out.printf("H");
				return 5;
				}*/
			if(inc[i]!=0){
				inc[i] += ant.getActiveFeromones(0,i);
				inc[i] -= 10*ant.getEnemyFeromones(i);
				if(inc[i]<0)
					inc[i]=0;
			}
		}

		if(ant.getStamina()<ant.getMaxStamina()){
			// incentive for moving forward
			inc[ant.getPreviousDir()] *= 4;

			// penalty for going back
			inc[Move.swapDir(ant.getPreviousDir())] *= 0.1;
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


