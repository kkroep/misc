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
        self.counterStrategy = 0
        self.juicyTargets = False
        self.juicyCorner = False
        self.floodGatesOpen = True
        self.defenseRating = 0
        self.defenseCost = 0

        self.mainStructure = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],\
        [ 27, 13],[ 9, 12],[ 10, 12],[ 11, 12],[ 12, 12],[ 13, 12],[ 14, 12],[ 15, 12],[ 16, 12],[ 17, 12],\
        [ 18, 12],[ 19, 12],[ 20, 12],[ 21, 12],[ 22, 12],[ 23, 12],[ 26, 12],[ 25, 11]]


        self.startingStructure = [[ 0, 13],[ 3, 13],[ 4, 13],[10, 12],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 27, 13],[ 9, 12],[ 11, 12],[ 12, 12],[ 13, 12],[ 14, 12],[ 26, 12]]
        
        self.essentialStructure = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 4, 13],[ 5, 13],[ 6, 13],[ 7, 13],[ 8, 13],\
        [ 9, 12],[ 10, 12],[ 11, 12],[ 12, 12],[ 13, 12],[ 14, 12],[ 15, 12],[ 26, 12],[ 27, 13]]

        self.encryptorStructure = [[ 18, 9],[ 19, 9],[ 13, 9]]
        self.extraEncryptorStructure = [[ 20, 9],[ 4, 9],[ 5, 9],[ 21, 9],[ 6, 9],[ 22, 9],[ 9, 9],[ 10, 9],[ 11, 9],[ 12, 9],[ 13, 9],[ 14, 9],[ 15, 9],[ 16, 9],[ 17, 9]]
        self.encryptorEmergencyStructure = [[ 4, 9],[ 5, 9]]

        self.extraDestructorLocs = [[24, 10], [23, 9],[ 22, 13],[ 23, 13],[ 24, 10],[ 23, 9],[ 23, 10]]
        self.extraDestructorLocs2 = [[ 9, 13],[ 12, 13],[ 15, 13],[ 18, 13]]

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
        if(game_state.turn_number == 0):
            locations = [[ 2, 12],[ 4, 12],[ 8, 12],[ 12, 12],[ 16, 12],[ 20, 12],[ 24, 12]]
            self.deploy(game_state, locations, FILTER)
            locations = [[ 4, 11],[ 8, 11],[ 12, 11],[ 16, 11],[ 20, 11],[ 24, 11]]
            self.deploy(game_state, locations, DESTRUCTOR)

        if(game_state.turn_number == 1):
            locations = [[ 6, 12]]
            self.deploy(game_state, locations, FILTER)
            locations = [[ 2, 11]]
            self.deploy(game_state, locations, DESTRUCTOR)

        if(game_state.turn_number == 2):
            locations = [[ 10, 12]]
            self.deploy(game_state, locations, FILTER)
            locations = [[ 6, 11]]
            self.deploy(game_state, locations, DESTRUCTOR)


        #gamelib.debug_write('essential structure missing {} parts, turn {}'.format(self.checkPresence(game_state, self.essentialStructure), game_state.turn_number))
        #self.repairCycle(game_state)
        #self.build_normal_structure(game_state)
        #self.deploy_attackers(game_state)



    # Here we make the C1 Logo!
    def first_turns(self, game_state):
        if game_state.turn_number == 0:
            self.exclusionList = [[1,13],[0,13],[10, 12]]
        else:
            # FLOODGATES STRATEGY
            if self.juicyCorner == False or self.juicyTargets == True:
                self.exclusionList = self.initExclusionList
                self.deploy(game_state, self.floodGate, FILTER)
                self.floodGatesOpen = False
            else:
                self.exclusionList = self.floodGate
                self.floodGatesOpen = True
                for location in self.floodGate:
                    if game_state.contains_stationary_unit(location):
                        self.remove(game_state, location)
                        self.floodGatesOpen = False

        firewall_locations = [[ 2, 13],[ 9, 12],[ 16, 12],[ 25, 11]] 
        self.deploy(game_state, firewall_locations, DESTRUCTOR)

        self.deploy(game_state, self.startingStructure, FILTER)
        self.deploy(game_state, self.essentialStructure, FILTER)
        self.deploy(game_state, self.mainStructure, FILTER)

    def analyzeOpponent(self, game_state):
        firewall_locations = game_state.game_map.get_all_enemy_firewall_locations()
        self.counterStrategy = 0
        
        # cycle to analyze where the EMP should be
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.x < 10 and unit.y < 16 and unit.unit_type == DESTRUCTOR and self.counterStrategy == 0:
                self.counterStrategy = 1
            if unit.x > 0 and unit.x < 16 and unit.y < 15 and unit.unit_type == DESTRUCTOR:
                self.counterStrategy = 2
            if unit.x > 0 and unit.x < 7 and unit.y < 15 and unit.unit_type == DESTRUCTOR:
                self.counterStrategy = 3
                break

        # cycle to analyze whether one should pump out pings or EMP's
        leftCornerFree = True
        leftCorner2Free = True
        leftCornerDangerFree = True
        count_EMP_path = 0
        for location in firewall_locations:
            unit = game_state.game_map[location][0]
            if unit.x < 16 and unit.y < 17:
                count_EMP_path += 1
            if unit.x < 4 and unit.y < 16 and unit.unit_type == DESTRUCTOR:
                leftCornerDangerFree = False
            if unit.x == 0 and unit.y == 14:
                leftCornerFree = False
            if unit.x == 1 and unit.y < 16:
                leftCorner2Free += 1

        if count_EMP_path > 6:
            self.juicyTargets = True
        else:
            self.juicyTargets = False

        leftCornerFree = leftCornerFree or leftCorner2Free
        if  leftCornerFree and leftCornerDangerFree:
            self.juicyCorner = True
        else:
            self.juicyCorner = False

    def repairCycle(self, game_state):
        firewall_locations = game_state.game_map.get_all_firewall_locations()
        counter = 2;
        if self.checkPresence(game_state, self.essentialStructure) > 2: # don't remove stuffwhen pressed for resources
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
        if(self.counterStrategy > 1): # all hands on deck, we need to kill those destructors
            self.deploy(game_state, firewall_locations, FILTER)
        else:
            self.remove(game_state, firewall_locations)

        # FLOODGATES STRATEGY
        if self.juicyCorner == False or self.juicyTargets == True:
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

        if game_state.get_resource(game_state.BITS) >= 6 and self.checkPresence(game_state, self.essentialStructure) > 2 and self.juicyTargets == True: # Priority to guide the attack if launched!
            self.deploy(game_state, self.essentialStructure, FILTER)

        self.deploy(game_state, self.essentialStructure, DESTRUCTOR)
        if(self.counterStrategy == 1 or self.counterStrategy == 3): # build encryptors to combat spawn destructors messing up stuff. Two is more than enough
            self.deploy(game_state, self.encryptorEmergencyStructure, ENCRYPTOR)
            if(game_state.CORES >= game_state.type_cost(ENCRYPTOR)):
                self.defenseRating = 1
        
        self.deploy(game_state, self.mainStructure, DESTRUCTOR)
        self.deploy(game_state, self.mainStructure, FILTER)

        self.deploy(game_state, self.extraDestructorLocs, DESTRUCTOR)
        self.deploy(game_state, self.encryptorStructure, ENCRYPTOR)
        self.deploy(game_state, self.extraDestructorLocs2, DESTRUCTOR)
        self.deploy(game_state, self.extraEncryptorStructure, ENCRYPTOR)

    def deploy_attackers(self, game_state):
        if self.counterStrategy < 2:
            PING_spawn = [[14,0]]
            SCRAMBLER_spawn = [[14,0]]
            EMP_spawn = [[2,11]]
        else:
            PING_spawn = [[14,0]]
            SCRAMBLER_spawn = [[2,11]]
            EMP_spawn = [[3,10]]

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
        if (game_state.turn_number == 0):
            self.deploy(game_state, PING_spawn, PING,5)
            return

        if (self.floodGatesOpen == True):
            self.deploy(game_state, PING_spawn, PING,5)
            self.deploy(game_state, PING_spawn, PING,2)
            self.deploy(game_state, PING_spawn, PING,2)
            self.deploy(game_state, PING_spawn, PING)
            self.deploy(game_state, PING_spawn, PING)

        if (game_state.get_resource(game_state.BITS) >= 6):
            self.deploy(game_state, EMP_spawn, EMP, 2)
            self.deploy(game_state, SCRAMBLER_spawn, SCRAMBLER)
            self.deploy(game_state, EMP_spawn, EMP)
            self.deploy(game_state, EMP_spawn, EMP)

        
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
