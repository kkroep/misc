import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""
    
def flipArray(array, flip):
    if flip == False:
        return array
    newArray = []
    for i in array:
        newArray.append([27-i[0], i[1]])
    return newArray



class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        self.prevHealth = 30
        self.flip = False
        self.futureFlip = False
        self.currentSide = 0
        self.PINGattack = True
        self.EMPattack = False
        self.DesM = False
        self.DesL = False
        self.DesR = False
        self.midDesR = False
        self.targetsL = 0
        self.targetsR = 0
        self.saveUp = False
        self.deployed = False
        self.deployed2 = False
        self.missingForSwitch = 0
        self.attackedLPrev = False
        self.attackedRPrev = False
        self.largeAttackOption = False
        self.pingRushL = False
        self.pingRushR = False

        self._1Fil = [[ 4, 13]]
        self._1Des = [[ 3, 13]]
        self._1Enc = [[ 7, 7]]
        
        self.edge = [[0, 13],[1, 12]]
        self.edge2 = [[3, 10],[4, 9],[5, 9],[6, 9]]
        self.edgeDes = [[2, 12]]
        self.edgeFil = [[1, 13]]

        self._2DesPriority = [[5, 12]]

        self._2Fil = [[ 5, 13],[ 6, 12],[ 7, 11],[ 8, 12],[ 12, 12]]
        self._2Des = [[10, 12],[5, 12]]
        self._2Enc = [[ 7, 8]]

        self._5DefOppFil = [[7,10]]
        self._5DefOppDes = [[7,9]]

        self._3Fil = [[ 12, 12],[ 13, 12],[ 14, 12],[ 15, 12]]
        self._3Des = [[ 11, 12]]
        self._3Enc = [[ 12, 8]]

        self.centerFil = [[9, 12], [11, 12]]

        self._4Des = [[ 5, 13],[ 10, 13]]
        self._4Fil = [[3,13],[13,13],[8,9],[9,9]]
        self._4Enc = [[ 9, 8]]

        #self.hoopla = [[5, 11]]
        self.hoopla = [[20, 10]]
        self.hoopla2 = [[6, 10]]

        self.gate = [[2, 13]]
        self.rank = [[11, 11]]
        
        self.flank = [[1,14],[2,15],[3,16]]
        self.flank2 = [[2,16],[3,15]]
        self.peekHole = [[15,12]]

        #self.haasjeOver = [[6,9],[7,7]]
        #self.haasjeOverExcl = [[ 5, 10],[ 6, 10],[ 5, 9],[ 5, 8],[ 6, 8],[ 6, 7]]

        self.pingRushFlank = [[3, 10], [4, 9],[5,10]]

        self.initExclusionList = [[0,0]]
        self.exclusionList = [[0,0]]

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        #gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """

    def detectPingRush(self, game_state):
        #self.pingRushL = False
        #self.pingRushR = False

        bits_he = game_state.get_resource(game_state.BITS,1)

        #path = game_state.find_path_to_edge([13, 0], 0)
        #for location in path:
                #if location[0] <= 3:
                #return
        target_edge = 3
        start_location = [13, 27]
        if not game_state.contains_stationary_unit(start_location):
            path = game_state.find_path_to_edge(start_location, target_edge)
            for location in path:
                if location[0] <= 1 or self.pingRushL:
                    self.pingRushL = True
                    self.attackedLPrev = True
                    self.deployed = True
                    #if bits_he <= 7:
                        #self.deploy(game_state, self.gate, FILTER, flip = False)
                    #self.deploy(game_state, self.pingRushFlank, FILTER, flip = False)
                    #self.remove(game_state, self.gate, flip = False)
                    #self.exclusionList.extend(self.gate)
                    self.deploy(game_state, [[3,13]], FILTER, flip = False)
                    self.deploy(game_state, [[0,13]], DESTRUCTOR, flip = False)
                    gamelib.debug_write('Ping rush left!, turn {}'.format(game_state.turn_number))
                    break

        #path = game_state.find_path_to_edge([14, 0], 1)
        #for location in path:
                #if location[0] >= 24:
                    #return

        target_edge = 2
        start_location = [14, 27]
        if not game_state.contains_stationary_unit(start_location):
            path = game_state.find_path_to_edge(start_location, target_edge)
            for location in path:
                if location[0] >= 26  or self.pingRushR:
                    self.pingRushR = True
                    self.attackedRPrev = True
                    self.deployed = True
                    #if bits_he < 8:
                        #self.deploy(game_state, self.gate, FILTER, flip = True)
                    #self.deploy(game_state, self.pingRushFlank, FILTER, flip = True)
                    #self.remove(game_state, self.gate, flip = True)
                    #self.deploy(game_state, self.hoopla, FILTER, flip = True)
                    #self.remove(game_state, self.gate, flip = True)
                    #self.exclusionList.extend(flipArray(self.gate, True))
                    self.deploy(game_state, [[3,13]], FILTER, flip = True)
                    self.deploy(game_state, [[0,13]], DESTRUCTOR, flip = True)
                    #gamelib.debug_write('Ping rush right!, turn {}'.format(game_state.turn_number))
                    break


    def starter_strategy(self, game_state):

        self.exclusionList = self.initExclusionList
        self.PINGattack = False
        self.EMPattack = False
        self.saveUp = False


        #self.detectPingRush(game_state)


        if game_state.turn_number != 0 :
            self.repairCycle(game_state)

        self.analyze(game_state)
        if self.currentSide == 0 or self.futureFlip != self.flip:
            self.buildUncertainty(game_state)

        self.deploy_attackers(game_state)


        if self.currentSide == 0 or self.futureFlip != self.flip:
            return
        self.buildFirewalls(game_state)

        #self.prevHealth = game_state.my_health

    def buildUncertainty(self, game_state):
        gateOpen = True
        if game_state.contains_stationary_unit(flipArray(self.edge2, self.futureFlip)[0]) or game_state.contains_stationary_unit(flipArray(self.gate, not self.futureFlip)[0]):
            gateOpen = False
            gamelib.debug_write('Cant switch yet, gate still closed, turn {}'.format(game_state.turn_number))

        self.remove(game_state, [self.edge2[0]],                flip =      self.flip)
        self.remove(game_state, [self.edge2[0]],                flip = not  self.flip)
        self.remove(game_state, self.gate,                      flip =      self.flip)
        self.remove(game_state, self.gate,                      flip = not  self.flip)


        core_cost = 0
        core_cost += self.checkMissing(game_state, self._1Fil,  flip = self.futureFlip)
        core_cost += self.checkMissing(game_state, self._2Fil,  flip = self.futureFlip)
        core_cost += self.checkMissing(game_state, self._3Fil,  flip = self.futureFlip)
        #core_cost += self.checkMissing(game_state, self.rank,   flip = self.futureFlip)
        core_cost += self.checkMissing(game_state, self.hoopla, flip = self.futureFlip)
        core_cost += self.checkMissing(game_state, self.gate,   flip = self.futureFlip)
        core_cost += self.checkMissing(game_state, self._1Des,  flip = self.futureFlip)*3
        core_cost += self.checkMissing(game_state, self._1Enc,  flip = self.futureFlip)*4

        cores_me = game_state.get_resource(game_state.CORES,0) 
        self.missingForSwitch = core_cost - cores_me

        if self.missingForSwitch > 0:
            gamelib.debug_write('cant afford switch, need {} have {}, turn {}'.format(core_cost, cores_me, game_state.turn_number))


        if (cores_me >= core_cost and self.currentSide != 0 and gateOpen == True):
            self.flip = self.futureFlip
            if self.futureFlip == True:
                self.currentSide = -1
            else:
                self.currentSide = 1
            gamelib.debug_write('SWITCH!!!!, turn {}'.format(game_state.turn_number))
            self.largeAttackOption = False
            self.deployed = True
            gamelib.debug_write('deployed by switching, turn {}'.format(game_state.turn_number))
            self.deploy(game_state, self._1Fil, FILTER,         flip =      self.flip)
            self.deploy(game_state, self._2Fil, FILTER,         flip =      self.flip)
            self.deploy(game_state, self._3Fil, FILTER,         flip =      self.flip)
            #self.deploy(game_state, self.rank, FILTER,          flip =      self.flip)
            self.deploy(game_state, self.hoopla, FILTER,        flip =      self.flip)
            self.deploy(game_state, self.gate, FILTER,          flip =      self.flip)
            self.deploy(game_state, self._1Des, DESTRUCTOR,     flip =      self.flip)
            self.deploy(game_state, self._1Enc, ENCRYPTOR,      flip =      self.flip)
        else:
            self.deploy(game_state, self._1Des, DESTRUCTOR,     flip =      self.flip)
            self.deploy(game_state, self._1Des, DESTRUCTOR,     flip = not  self.flip)
            self.deploy(game_state, self._1Fil, FILTER,         flip =      self.flip)
            self.deploy(game_state, self._1Fil, FILTER,         flip = not  self.flip)
            self.deploy(game_state, self.edge, FILTER,          flip =      self.flip)
            self.deploy(game_state, self.edge, FILTER,          flip = not  self.flip)

    def buildFirewalls(self, game_state):
        # gate and hoopla management
        self.deploy(game_state, self.gate, FILTER,              flip =      self.flip)

        if self.deployed == True:
            self.remove(game_state, self.gate,                  flip = not  self.flip)
        else:
            self.deploy(game_state, self.gate, FILTER,          flip = not  self.flip)

        #self.remove(game_state, self.haasjeOverExcl,        flip =      self.flip)

        #self.remove(game_state, self.hoopla,                    flip = not  self.flip)
        self.deploy(game_state, self.hoopla2, FILTER,            flip =      self.flip)


        self.deploy(game_state, self._1Des, DESTRUCTOR,         flip =      self.flip)
        self.deploy(game_state, self._2Fil, FILTER,             flip =      self.flip)
        self.deploy(game_state, self._1Fil, FILTER,             flip =      self.flip)
        self.deploy(game_state, self._2Des, DESTRUCTOR,         flip =      self.flip)
        self.deploy(game_state, self._1Enc, ENCRYPTOR,          flip =      self.flip)

        self.deploy(game_state, self.edge, FILTER,              flip =      self.flip)
        self.deploy(game_state, self.edge, FILTER,              flip = not  self.flip)
        if self.deployed == False:
            self.deploy(game_state, self.centerFil, FILTER,             flip =      self.flip)

        self.deploy(game_state, self._5DefOppDes, DESTRUCTOR,         flip = not  self.flip)
        self.deploy(game_state, self._5DefOppDes, FILTER,             flip = not  self.flip)


        # finally first encryptor
        if (self.enemyEncR > 0 and self.flip == True) or (self.enemyEncL > 0 and self.flip == False):
            self.deploy(game_state, self._2Des, DESTRUCTOR,         flip =      self.flip)
            self.deploy(game_state, self._2Enc, ENCRYPTOR,          flip =      self.flip)
            if self.saveUp == True:
                gamelib.debug_write('Trying to build emergency 3st encryptor, but cant afford, turn {}'.format(game_state.turn_number))
                return

        if self.saveUp == False:
            location = flipArray(self._2Des, not self.flip)[1]
            if game_state.contains_stationary_unit(location):
                unit = game_state.game_map[location][0]
                if unit.unit_type == FILTER:
                    self.remove(game_state, [location], flip = False)

        self.deploy(game_state, self._1Enc, ENCRYPTOR,          flip =      self.flip)
        self.deploy(game_state, self._3Fil, FILTER,             flip =      self.flip)

        # if crossing another filter, counter with filter
        if (self.enemyEncR > 0 and self.flip == False) or (self.enemyEncL > 0 and self.flip == True):
            self.deploy(game_state, self._2Enc, ENCRYPTOR,      flip =      self.flip)

        if self.saveUp == False and self.deployed == False:
            self.deployed = True
            gamelib.debug_write('deployed by building, turn {}'.format(game_state.turn_number))


        #if self.largeAttackOption == True:
            #self.deploy(game_state, self.haasjeOver, FILTER,     flip =      self.flip)

        # counter  extra on EMP line combat:
        #if (self.enemyEncR > 0 and self.flip == True) or (self.enemyEncL > 0 and self.flip == False):

        # resulting build up chunk
        
        # vangrail
        self.remove(game_state, [self.edge2[0]],                flip =      self.flip)
        if self.deployed == True:
            self.deploy(game_state, self.edge2, FILTER,         flip = not  self.flip)
            self.deploy(game_state, self.hoopla, FILTER,            flip =      self.flip)
            #self.deploy(game_state, self.hoopla2, FILTER,            flip = not self.flip)

        self.deploy(game_state, self._2Des, DESTRUCTOR,         flip = not  self.flip)

        # remove filter that is no longer necesarry
        if self.saveUp == False:
            location = flipArray(self._2Des, self.flip)[1]
            if game_state.contains_stationary_unit(location):
                unit = game_state.game_map[location][0]
                if unit.unit_type == FILTER:
                    self.remove(game_state, [location], flip = False)

        self.deploy(game_state, self._2Des, DESTRUCTOR,         flip =      self.flip)
        self.deploy(game_state, self._2Fil, FILTER,             flip = not  self.flip)


        #self.deploy(game_state, self._1Enc, ENCRYPTOR,          flip = not  self.flip)
        self.deploy(game_state, self._2Enc, ENCRYPTOR,          flip =      self.flip)

        self.deploy(game_state, self._4Fil, FILTER,             flip = not  self.flip)
        self.deploy(game_state, self._4Fil, FILTER,             flip =      self.flip)
        self.deploy(game_state, self._2Enc, ENCRYPTOR,          flip = not  self.flip)


        if self.saveUp == False:
            location = flipArray(self._3Des, not self.flip)[0]
            if game_state.contains_stationary_unit(location):
                unit = game_state.game_map[location][0]
                if unit.unit_type == FILTER:
                    self.remove(game_state, [location], flip = False)


        self.deploy(game_state, self._3Des, DESTRUCTOR,         flip = not  self.flip)
        if self.saveUp == False:
            self.remove(game_state, self.peekHole,              flip =      self.flip)
            gamelib.debug_write('Peeping tom!, turn {}'.format(game_state.turn_number))


        self.deploy(game_state, self._3Enc, ENCRYPTOR,          flip =      self.flip)
        self.deploy(game_state, self._3Enc, ENCRYPTOR,          flip = not  self.flip)

        if self.saveUp == False:
            location = flipArray(self._3Des, self.flip)[0]
            if game_state.contains_stationary_unit(location):
                unit = game_state.game_map[location][0]
                if unit.unit_type == FILTER:
                    self.remove(game_state, [location], flip = False)

        self.deploy(game_state, self._3Des, DESTRUCTOR,         flip =      self.flip)
        self.deploy(game_state, self._4Enc, ENCRYPTOR,          flip = not  self.flip)
        self.deploy(game_state, self._4Enc, ENCRYPTOR,          flip =      self.flip)


        self.deploy(game_state, self._4Des, DESTRUCTOR,         flip =      self.flip)
        self.deploy(game_state, self._4Des, DESTRUCTOR,         flip = not  self.flip)

    def analyze(self, game_state):
        self.targetsL = 0
        self.targetsR = 0
        self.enemyEncL = 0
        self.enemyEncR = 0
        totalL = 0
        totalR = 0

        firewall_locations = game_state.game_map.get_all_enemy_firewall_locations()
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.x >= 14:
                if unit.unit_type == ENCRYPTOR and unit.x >= 16 and unit.y <= 19:
                    self.enemyEncR += 1
                    totalR += 2
                else:
                    totalR += 1
            else:
                if unit.unit_type == ENCRYPTOR and unit.x <= 11 and unit.y <= 19:
                    self.enemyEncL += 1
                    totalL += 2
                else:
                    totalL += 1
            if unit.y < 18:
                if unit.x <= 13 and unit.x >= 3 and unit.y <= 16:
                    self.targetsL += 1 
                    if unit.unit_type == DESTRUCTOR:
                        self.targetsL += 1
                    if unit.unit_type == ENCRYPTOR:
                        self.targetsL += 2
                elif unit.x <= 24 and unit.x >= 14 and unit.y <= 16:
                    self.targetsR += 1
                    if unit.unit_type == DESTRUCTOR:
                        self.targetsR += 1
                    if unit.unit_type == ENCRYPTOR:
                        self.targetsR += 2


        if game_state.turn_number != 0 and self.currentSide == 0:
            if self.targetsR > self.targetsL:
                self.currentSide = -1
                self.flip = True
            elif self.targetsL > self.targetsR or self.targetsL >= 8:
                self.currentSide = 1
                self.flip = False
            elif totalR > totalL:
                self.currentSide = -1
                self.flip = True
            elif totalL > totalR or totalL >= 10:
                self.currentSide = 1
                self.flip = False
            else:
                gamelib.debug_write('cant choose sides targetsL {} targetsR {}, turn {}'.format(self.targetsL, self.targetsR, game_state.turn_number))


        self.DesL = False
        self.DesM = False
        self.DesR = False

        if game_state.turn_number == 0:
            return

        firewall_locations = game_state.game_map.get_all_enemy_firewall_locations()
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.y == 14 and unit.unit_type == DESTRUCTOR:
                if unit.x >= 5 and unit.x <= 11:
                    self.DesL = True
                if unit.x >= 11 and unit.x <= 16:
                    self.DesM = True
                if unit.x >= 16 and unit.x <= 22:
                    self.DesR = True

        if self.DesL == True or self.DesM == True:        
            self.deploy(game_state, self.rank, FILTER,              flip = False)

        if self.DesR == True or self.DesM == True:        
            self.deploy(game_state, self.rank, FILTER,              flip = True)

        if self.DesL == False and self.DesM == False:
            self.remove(game_state, self.rank,                      flip = True)

        if self.DesR == False and self.DesM == False:
            self.remove(game_state, self.rank,                      flip = False)

        alreadyFlipping = False
        if self.futureFlip != self.flip:
            alreadyFlipping = True

        self.futureFlip = self.flip
        if (self.flip == False and self.targetsL <= 8 and self.targetsL + 8 <= self.targetsR):
            #self.futureFlip = True
            return
      
        if (self.flip == True and self.targetsR <= 8 and self.targetsR + 8 <= self.targetsL):
            #self.futureFlip = False
            return

        if alreadyFlipping == True and self.futureFlip == self.flip:
            gamelib.debug_write('No longer considering flipping :) targetsL {} targetsR {}, turn {}'.format(self.targetsL, self.targetsR, game_state.turn_number))


    def repairCycle(self, game_state):
        counter = 2;

        """for flipper in [True, False]:
            attacked = False
            if self.checkMissing(game_state, self.flank, flip = flipper) == 3 and self.checkMissing(game_state, self.flank2, flip = flipper) > 0:
                locations = flipArray(self.edge, flip = flipper)
                for location in locations:
                    if self.checkMissing(game_state, [location]) > 0:
                        self.deploy(game_state, [location], DESTRUCTOR)
                        self.deploy(game_state, [location], FILTER)
                        if flipper == True:
                            self.attackedRPrev = True
                        else:
                            self.attackedLPrev = True
                    else:
                        unit = game_state.game_map[location][0]
                        if unit.stability < 60:
                            self.remove(game_state, [location])
                            counter = 1
                            if flipper == True:
                                self.attackedRPrev = True
                            else:
                                self.attackedLPrev = True
            else:
                if flipper == True:
                    self.attackedRPrev = False
                else:
                    self.attackedLPrev = False

        # gate is vulnerable part of structure
        gate = flipArray(self.gate, self.flip)[0]
        if game_state.contains_stationary_unit(gate):
            unit = game_state.game_map[gate][0]
            if unit.stability < 30:
                self.remove(game_state, self.gate, flip = self.flip)
                counter -= 1

        if self.attackedLPrev == True: # if the corner we spawn from
            #self.deploy(game_state, self.edgeDes, DESTRUCTOR, flip = False) # kijkhier naar!
            #self.deploy(game_state, self.edgeFil, FILTER, flip = False) # kijkhier naar!
            gamelib.debug_write('prev attacked at L, turn {}'.format(game_state.turn_number))


        if self.attackedRPrev == True: # if the corner we spawn from
            #self.deploy(game_state, self.edgeDes, DESTRUCTOR, flip = True) # kijkhier naar!
            #self.deploy(game_state, self.edgeFil, FILTER, flip = True) # kijkhier naar!
            gamelib.debug_write('prev attacked at R, turn {}'.format(game_state.turn_number))
        """

        firewall_locations = game_state.game_map.get_all_firewall_locations()
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if (unit.stability < 25 and not unit.unit_type == ENCRYPTOR):
                #gamelib.debug_write('({}, {}), reparing for {} stability'.format(location[0], location[1], unit.stability))
                if game_state.contains_stationary_unit(location):
                    game_state.attempt_remove(location)
                    counter -= 1
                    if counter == 0:
                        break    

    def deploy_attackers(self, game_state, flip = False):

        DEF_S = flipArray([[18,4]], self.flip)
        DEF2_S = flipArray([[14,0]], self.flip)
        RUSH_S = flipArray([[4,9]], self.flip)
        S3 = flipArray([[3,10]], self.flip)
        S4 = flipArray([[4,9]], self.flip)
        ALT_S = flipArray([[6,7]], self.flip)

        #if game_state.contains_stationary_unit(S3[0]):
            #S3 = ALT_S 

        if self.flip == False:
            target_edge = 0
        else:
            target_edge = 1

        bits_me = game_state.get_resource(game_state.BITS,0)
        bits_he = game_state.get_resource(game_state.BITS,1)

        gate = flipArray(self.gate, flip = True)[0]

        if(game_state.turn_number < 1):
            self.deploy(game_state, [[13,0]], PING, 10)
            self.PINGattack = True
            return

        if game_state.contains_stationary_unit(S3[0]):
            gamelib.debug_write('Attack ERROR, havent removed start yet!!!!!, turn {}'.format(game_state.turn_number))
            return
        damage =  self.checkReceivedDamage(game_state, S3[0], 1000 ,target_edge) 
        if damage[2]<13:
            gamelib.debug_write('Attack ERROR!!!!!, turn {}'.format(game_state.turn_number))
            return # smash head against my own wall stupid

        #if damage[0] == 1000: # gaat tegegn blokkade oplopen, leuk :D BOMMETJE
            #self.deploy(game_state, SCR_S, SCRAMBLER, 2)
        # misschien uitzoeken of ik hier iets mee kan? 


        if (self.targetsL >= 8 and self.currentSide == 1) or (self.targetsR >= 8 and self.currentSide == -1):
            self.deploy(game_state, S4, SCRAMBLER, 2)
            gamelib.debug_write('normal attack, turn {}'.format(game_state.turn_number))
            self.deploy(game_state, S3, EMP)
            self.EMPattack = True
            return
        
        # ping attack?

        damage_LB = self.checkReceivedDamage(game_state, [13,0], 1000 ,0) # 0 is top right, 1 is top legft
        steps_LB = len(game_state.find_path_to_edge([13,0], 0))

        damage_LM = self.checkReceivedDamage(game_state, [6,7], 1000 ,0) # 0 is top right, 1 is top legft
        steps_LM = len(game_state.find_path_to_edge([7,6], 0))
        
        damage_RB = self.checkReceivedDamage(game_state, [14,0], 1000 ,1) # 0 is top right, 1 is top legft
        steps_RB = len(game_state.find_path_to_edge([14,0], 1))
        
        damage_RM = self.checkReceivedDamage(game_state, [21,7], 1000 ,1) # 0 is top right, 1 is top legft
        steps_RM = len(game_state.find_path_to_edge([20,6], 1))

        damage = damage_LB[0]
        steps = steps_LB
        target_edge = 0
        PING_S = [[13,0]]
        unit_type = PING
        if damage_LM[0] < damage or (damage_LM[0] == damage and steps_LM < steps): 
            damage = damage_LM[0]
            PING_S = [[6,7]]
            steps = steps_LM
            unit_type = SCRAMBLER
        if damage_RB[0] < damage or (damage_RB[0] == damage and steps_RB < steps): 
            damage = damage_RB[0]
            PING_S = [[14,0]]
            target_edge = 1
            steps = steps_RB
            unit_type = PING
        if damage_RM[0] < damage or (damage_RM[0] == damage and steps_RM < steps): 
            damage = damage_RM[0]
            PING_S = [[21,7]]
            target_edge = 1
            steps = steps_RM
            unit_type = SCRAMBLER


        if damage < bits_me * 15: 
            gamelib.debug_write('attacking from {} losing {} health with {} steps, turn {}'.format(PING_S, damage, steps, game_state.turn_number))
            if bits_he >= 10:
                self.deploy(game_state, PING_S, SCRAMBLER)
            else:
                self.deploy(game_state, PING_S, SCRAMBLER)
            self.exclusionList = game_state.find_path_to_edge(PING_S[0], target_edge)

            self.PINGattack = True
            return
        else:
            gamelib.debug_write('not going for attack from {} losing {} health, turn {}'.format(PING_S, damage, game_state.turn_number))

        # maybe we are getting attacked?
        if bits_he >= 10 and bits_me < 9:
            self.deploy(game_state, DEF_S, SCRAMBLER, 1)
        if bits_he >= 14 and bits_me < 10:
            self.deploy(game_state, DEF2_S, SCRAMBLER, 1)

        if self.flip != self.futureFlip:
            return


        bits_me = game_state.get_resource(game_state.BITS,0)

        # then maybe still an EMP attack, or save up?
        if ((self.pingRushL and self.currentSide == 1) or (self.pingRushR and self.currentSide == -1)) and bits_me >= 6:
            self.deploy(game_state, S4, SCRAMBLER, 1)
            self.deploy(game_state, S3, EMP)
            self.EMPattack = True
            return
            
        self.largeAttackOption = True

        #if (bits_me >= 8 and self.checkMissing(game_state, self.haasjeOver, flip = self.flip) == 0):
            #self.deploy(game_state, EMP_S, SCRAMBLER, 2)
            #self.deploy(game_state, ALT_S, EMP)
            #return

        if bits_me >= 7:
            self.deploy(game_state, S3, EMP)
            return 

        gamelib.debug_write('still no attack options, turn {}'.format(game_state.turn_number))

    def deploy(self, game_state, locations, unit_type, amount=20, flip = False):
        isFirewall = (unit_type == FILTER or unit_type == DESTRUCTOR or unit_type == ENCRYPTOR)
        if self.saveUp == True and isFirewall:
            return
        new_locations = flipArray(locations, flip)
        for i in range(amount):
            for location in new_locations:
                exclude = False
                for exclusion in self.exclusionList:
                    if exclusion == location:
                        exclude = isFirewall
                        break
                if game_state.can_spawn(unit_type, location, 1) and not exclude:
                    game_state.attempt_spawn(unit_type, location, 1)
                if game_state.contains_stationary_unit(location) == False and not exclude and isFirewall:
                    self.saveUp = True
                    return

    def checkReceivedDamage(self, game_state, start_location, health, target_edge):
        path = game_state.find_path_to_edge(start_location, target_edge)
        endpoint = path[-1]
        if (endpoint[1]-endpoint[0] != 14 and target_edge == 1) or (endpoint[0]+endpoint[1] != 41 and target_edge == 0):
            #gamelib.debug_write('cant reach edge. Path length {}, last point ({},{}), turn {}'.format(len(path), endpoint[0], endpoint[1], game_state.turn_number))
            return [10000, endpoint[0], endpoint[1]]   
        damage = 0.0
        for location in path:
            inRange = game_state.game_map.get_locations_in_range(location, 3.5)
            for target in inRange:
                if target[1] > 13 and game_state.contains_stationary_unit(target):
                    unit = game_state.game_map[target][0]
                    if unit.unit_type == DESTRUCTOR:
                        damage += 16.0
                        if damage >= health:
                            endpoint = location
                            return [damage, endpoint[0], endpoint[1]]
        return [damage, endpoint[0], endpoint[1]]

    def checkDealtDamage(self, game_state, start_location, target_location):
        path = game_state.find_path_to_point(start_location, target_location)
        damage = 0
        steps = len(path)
        for location in path:
            inRange = game_state.game_map.get_locations_in_range(location, 5.5)
            for target in inRange:
                if target[1] > 13 and game_state.contains_stationary_unit(target):
                    damage += 1
                    break
        return [damage, steps]

    def checkMissing(self, game_state, locations, flip = False):
        counter = 0
        new_locations  = flipArray(locations, flip)
        for location in new_locations:
            #exclude = False
            #for exclusion in self.exclusionList:
                #if exclusion == location:
                    #exclude = True
                    #break
            #if exclude == False and not game_state.contains_stationary_unit(location):
            if not game_state.contains_stationary_unit(location):
                counter += 1
        return counter

    def remove(self, game_state, locations, flip = False):
        removed = False
        locations = flipArray(locations, flip)
        for location in locations:
            if game_state.contains_stationary_unit(location):
                if game_state.attempt_remove(location) != None:
                    removed = True
        return removed

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
