import os
from enum import Enum
from random import shuffle 

'''
Simple statemachine for mobgame.

'''
class GameState(Enum):
    STOPPED = 1
    RUNNING = 2
    EXPIRED = 3

MobPopulation = ['zombie', ]    

class Mobgame:
    def __init__(self):
        self.state = GameState.STOPPED
        self.scoreboard = dict()

    
        
        

        
