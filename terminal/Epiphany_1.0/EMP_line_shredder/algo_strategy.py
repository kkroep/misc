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
        self.structureInPlace = False
        self.destructorsLeft = 0
        self.destructorsMiddle = 0
        self.juicyTargets = 0
        self.juicyCorner = False
        self.floodGatesOpen = True
        self.defenseRating = 0
        self.defenseCost = 0
        self.attackedFromLeft = 0

        self.mainStructure = [[ 25, 13],[ 24, 12],[ 23, 11],[ 22, 10],[ 21, 9],[ 20, 8],[ 19, 7],[ 18, 6],[ 17, 5],[ 16, 4],[ 15, 3],[ 14, 2],[ 13, 1]]


        self.startingStructure = [[ 25, 13],[ 24, 12],[ 23, 11],[ 22, 10],[ 21, 9],[ 20, 8],[ 19, 7],[ 18, 6],[ 17, 5],[ 16, 4],[ 15, 3],[ 14, 2],[ 13, 1]]
        self.essentialStructure = [[ 25, 13],[ 24, 12],[ 23, 11],[ 22, 10],[ 21, 9],[ 20, 8],[ 19, 7],[ 18, 6],[ 17, 5],[ 16, 4],[ 15, 3],[ 14, 2],[ 13, 1]]

        self.encryptorStructure = [[ 21, 9]]
        self.extraEncryptorStructure = [[ 21, 10],[ 20, 9]]
        self.extraEncryptorStructure2 = [[ 19, 10],[ 20, 10],[ 21, 10],[ 19, 9],[ 20, 9]]
        self.encryptorEmergencyStructure = [[ 4, 9],[ 5, 9]]

        self.extraDestructorLocs = [[ 25, 13]]
        self.extraDestructorLocs2 = [[ 0, 13],[ 1, 12],[ 2, 11],[ 3, 10],[ 4, 9]]
        self.extraDestructorLocs3 = [[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 5, 8],[ 6, 7],[ 7, 6],[ 8, 5],[ 9, 4],[ 10, 3],[ 11, 2]]

        self.initExclusionList = [[0,0]]
        self.exclusionList = [[0,0]]
        self.floodGate = [[1,13],[0,13]]

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
    def starter_strategy(self, game_state):

        #self.analyzeOpponent(game_state)
        #if(game_state.turn_number < 20):
        self.first_turns(game_state)

        #gamelib.debug_write('essential structure missing {} parts, turn {}'.format(self.checkMissing(game_state, self.essentialStructure), game_state.turn_number))
        #self.repairCycle(game_state)
        #self.build_normal_structure(game_state)
        self.deploy_attackers(game_state)



    # Here we make the C1 Logo!
    def first_turns(self, game_state):
        self.deploy(game_state, self.extraDestructorLocs, DESTRUCTOR)

        self.deploy(game_state, self.encryptorStructure, ENCRYPTOR)
        self.deploy(game_state, self.essentialStructure, FILTER)
        self.deploy(game_state, self.mainStructure, FILTER)
        self.deploy(game_state, self.extraDestructorLocs2, DESTRUCTOR)
        self.deploy(game_state, self.extraEncryptorStructure, ENCRYPTOR)
        self.deploy(game_state, self.extraEncryptorStructure2, ENCRYPTOR)
        self.deploy(game_state, self.extraDestructorLocs3, DESTRUCTOR)

    def analyzeOpponent(self, game_state):
        
        # analyze wether the left side is being attacked, and act accordingly
        self.attackedFromLeft -= 1
        if self.floodGatesOpen == False: #if the nodes aren't destroyed because of me
            locations = [[0, 13], [1, 13]]
            for location in locations:
                if not game_state.contains_stationary_unit(location):
                    self.attackedFromLeft = 5
                    break


        firewall_locations = game_state.game_map.get_all_enemy_firewall_locations()
        self.destructorsLeft = 0
        self.destructorsMiddle = 0

        # cycle to analyze where the EMP should be
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.x > 0 and unit.x < 7 and unit.y < 15 and unit.unit_type == DESTRUCTOR:
                self.destructorsLeft = 2
            if unit.x > 0 and unit.x < 8 and unit.y < 16 and unit.unit_type == DESTRUCTOR and self.destructorsLeft == 0:
                self.destructorsLeft = 1
            if unit.x > 0 and unit.x < 16 and unit.y < 15 and unit.unit_type == DESTRUCTOR:
                self.destructorsMiddle = 1

        # cycle to analyze whether one should pump out pings or EMP's
        leftCornerFree = True
        leftCorner2Free = True
        leftCornerDangerFree = True
        count_EMP_path = 0
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.x > 2 and unit.x < 16 and unit.y < 17:
                if unit.unit_type == FILTER:
                    count_EMP_path += 1
                else:
                    count_EMP_path += 2
            if unit.x < 4 and unit.y < 16 and unit.unit_type == DESTRUCTOR:
                leftCornerDangerFree = False
            if unit.x == 0 and unit.y == 14:
                leftCornerFree = False
            if unit.x == 1 and unit.y < 16:
                leftCorner2Free = False

        self.juicyTargets = count_EMP_path

        leftCornerFree = leftCornerFree or leftCorner2Free
        if  leftCornerFree and leftCornerDangerFree:
            self.juicyCorner = True
        else:
            self.juicyCorner = False

    def repairCycle(self, game_state):
        firewall_locations = game_state.game_map.get_all_firewall_locations()
        counter = 2;
        if self.checkMissing(game_state, self.essentialStructure) > 2: # don't remove stuffwhen pressed for resources
            return
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.stability < 25 and not unit.unit_type == ENCRYPTOR:
                gamelib.debug_write('({}, {}), reparing for {} stability'.format(location[0], location[1], unit.stability))
                if game_state.contains_stationary_unit(location):
                    game_state.attempt_remove(location)
                    counter -= 1
                    if counter == 0:
                        break    

    def build_normal_structure(self, game_state):
        firewall_locations = [[8, 11], [16, 11]]
        if (self.destructorsLeft == 2 and self.defenseRating == 0) or self.destructorsMiddle == 1: # all hands on deck, we need to kill those destructors
            self.deploy(game_state, firewall_locations, FILTER)
        else:
            self.remove(game_state, firewall_locations)

        # FLOODGATES STRATEGY
        if self.attackedFromLeft > 0:
            self.exclusionList = self.initExclusionList
            self.deploy(game_state, self.floodGate, DESTRUCTOR)
            self.floodGatesOpen = False
        elif self.juicyCorner == False or self.juicyTargets > 6:
            self.exclusionList = self.initExclusionList
            self.deploy(game_state, self.floodGate, FILTER)
            self.floodGatesOpen = False
        else:
            self.exclusionList = self.floodGate
            if game_state.contains_stationary_unit(self.floodGate[0]):
                self.remove(game_state, self.floodGate)
                self.floodGatesOpen = False
            else:
                self.floodGatesOpen = True

        if game_state.get_resource(game_state.BITS) >= 6 and self.checkMissing(game_state, self.essentialStructure) > 2 and self.juicyTargets > 6: # Priority to guide the attack if launched!
            self.deploy(game_state, self.essentialStructure, FILTER)

        self.deploy(game_state, self.essentialStructure, DESTRUCTOR)
        if(self.destructorsLeft == 2): # build encryptors to combat spawn destructors messing up stuff. Two is more than enough
            self.deploy(game_state, self.encryptorEmergencyStructure, ENCRYPTOR)
            if(game_state.CORES >= game_state.type_cost(ENCRYPTOR)):
                self.defenseRating = 1
        
        self.deploy(game_state, self.mainStructure, DESTRUCTOR)
        self.deploy(game_state, self.mainStructure, FILTER)

        self.deploy(game_state, self.extraDestructorLocs, DESTRUCTOR)
        self.deploy(game_state, self.encryptorStructure, ENCRYPTOR)
        self.deploy(game_state, self.extraDestructorLocs2, DESTRUCTOR)
        self.deploy(game_state, self.extraEncryptorStructure, ENCRYPTOR)
        self.deploy(game_state, self.extraDestructorLocs3, DESTRUCTOR)

    def deploy_attackers(self, game_state):
        SCARMBLER_defense_spawn = [[14,0]]
        SCARMBLER_defense_spawn2 = [[18,4]]

        if (self.destructorsLeft == 2 and self.defenseRating == 0) or self.destructorsMiddle != 0: 
            PING_spawn = [[14,0]]
            SCRAMBLER_spawn = [[2,11]]
            EMP_spawn = [[3,10]]
        else:
            PING_spawn = [[14,0]]
            SCRAMBLER_spawn = [[14,0]]
            EMP_spawn = [[2,11]]

        PING_spawn = [[13,0]]
        """
        if(game_state.get_resource(game_state.BITS,1)>=9+self.defenseRating):
            self.deploy(game_state, SCRAMBLER_spawn, SCRAMBLER, 1)
            self.deploy(game_state, [[19, 5]], SCRAMBLER, 1)
            gamelib.debug_write('PREVENTING ATTACK! turn {}'.format(game_state.turn_number))
        if(game_state.get_resource(game_state.BITS,1)>=12+self.defenseRating):
            self.deploy(game_state, [[19, 5]], SCRAMBLER, 1)
            self.deploy(game_state, [[13, 0]], SCRAMBLER, 1)
            gamelib.debug_write('PREVENTING HUUUUGE ATTACK! turn {}'.format(game_state.turn_number))
        """

        #if (game_state.turn_number == 0):
        self.deploy(game_state, PING_spawn, PING,5)
        self.deploy(game_state, PING_spawn, PING,1)
        self.deploy(game_state, PING_spawn, PING,1)
        return

        if (self.floodGatesOpen == True):
            self.deploy(game_state, PING_spawn, PING,5)
            self.deploy(game_state, PING_spawn, PING,2)
            self.deploy(game_state, PING_spawn, PING,2)
            self.deploy(game_state, PING_spawn, PING)
            self.deploy(game_state, PING_spawn, PING)

        
        if self.juicyTargets > 10:
            if (game_state.get_resource(game_state.BITS) >= 12):
                self.deploy(game_state, EMP_spawn, EMP, 4)
                self.deploy(game_state, SCRAMBLER_spawn, SCRAMBLER)
                self.deploy(game_state, EMP_spawn, EMP)
                self.deploy(game_state, EMP_spawn, EMP)
        elif self.juicyTargets > 5:
            if (game_state.get_resource(game_state.BITS) >= 6):
                self.deploy(game_state, EMP_spawn, EMP, 2)
                self.deploy(game_state, SCRAMBLER_spawn, SCRAMBLER)
        else:
            if(game_state.get_resource(game_state.BITS,1)>=14):
                self.deploy(game_state, SCARMBLER_defense_spawn, SCRAMBLER)
            if(game_state.get_resource(game_state.BITS,1)>=10):
                self.deploy(game_state, SCARMBLER_defense_spawn, SCRAMBLER)
                self.deploy(game_state, SCARMBLER_defense_spawn2, SCRAMBLER)
            if (game_state.get_resource(game_state.BITS) >= 8):
                self.deploy(game_state, EMP_spawn, PING,8)

        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def deploy(self, game_state, locations, unit_type, amount=1):
        for location in locations:
            exclude = False
            for exclusion in self.exclusionList:
                if exclusion == location:
                    exclude = True
                    break
            if game_state.can_spawn(unit_type, location, amount) and not exclude:
                game_state.attempt_spawn(unit_type, location, amount)

    def checkMissing(self, game_state, locations):
        counter = 0
        for location in locations:
            exclude = False
            for exclusion in self.exclusionList:
                if exclusion == location:
                    exclude = True
                    break
            if exclude == False and not game_state.contains_stationary_unit(location):
                counter += 1
        return counter


    def remove(self, game_state, locations):
        for location in locations:
            if game_state.contains_stationary_unit(location):
                game_state.attempt_remove(location)

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
