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


        self.filter0 =[[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],\
        [ 9, 13],[ 10, 13],[ 17, 13],[ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 25, 13],[ 26, 13],[ 27, 13]] 
        self.filter1 = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 17, 13],\
        [ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 25, 13],[ 26, 13],[ 27, 13],[ 2, 12],[ 25, 12],[ 3, 11],[ 24, 11],[ 4, 10]]
        self.filter2 =  [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 17, 13],\
        [ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 25, 13],[ 26, 13],[ 27, 13],[ 2, 12],[ 25, 12],[ 3, 11],[ 24, 11],[ 4, 10]]
        self.filter3 = [[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13]]

        self.destructor0 = [[ 13, 13]]
        self.destructor1 = [[ 13, 13],[ 14, 13]]
        self.destructor2 = [[ 13, 13],[ 14, 13]]
        self.destructor3 = [[ 13, 13],[ 14, 13]]

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
    def starter_strategy(self, game_state):

        #self.analyzeOpponent(game_state)
        #if(game_state.turn_number < 20):
        #self.first_turns(game_state)

        if game_state.turn_number == 0 :
            self.deploy(game_state, self.filter0, FILTER)
            self.deploy(game_state, self.destructor0, DESTRUCTOR)
        elif game_state.turn_number == 1 :
            self.deploy(game_state, self.filter1, FILTER)
            self.deploy(game_state, self.destructor1, DESTRUCTOR)
        elif game_state.turn_number == 2 :
            self.deploy(game_state, self.filter2, FILTER)
            self.deploy(game_state, self.destructor2, DESTRUCTOR)
        elif game_state.turn_number > 2 :
            self.deploy(game_state, self.filter3, FILTER)
            self.deploy(game_state, self.destructor3, DESTRUCTOR)
            self.remove(game_state,[[ 13, 13],[ 14, 13],[ 18, 13]])

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
        if game_state.turn_number == 0:
            self.deploy(game_state, [[ 23, 9]], PING,2)
            self.deploy(game_state, [[ 23, 9]], EMP,1)
            return
        if game_state.turn_number ==3:
            self.deploy(game_state, [[ 23, 9]], PING,4)
            self.deploy(game_state, [[ 23, 9]], EMP,2)
            return

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
