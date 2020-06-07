import os
import time
from enum import Enum
from random import shuffle 

'''
Simple statemachine for mobgame.

'''
class GameState(Enum):
    STOPPED = 1
    RUNNING = 2
    EXPIRED = 3

SEC_EXPIRE_DURATION = 3 * 60    # 3 minutes

# To be adjusted: Jake is working on it.
MobPopulation = ['zombie', 'dwarf', 'brute', 'ettin', 'frog', 'earthworm', 'rabbit', 'buffalo', 'gnome', 'kraken' ]
BossPopulation = ['amphisbaena', 'canocephalus', 'mermicolion']

class Mobgame:
    def __init__(self):
        self.reset()
        self.startAt = 0
        self.expireAt = 0

    def reset(self):
        self.state = GameState.STOPPED
        self.scoreboard = dict()
        self.mobs = []
        self.boss = []
    
    def setup(self):
        self.startAt = time.time()
        self.expireAt = time.time() + SEC_EXPIRE_DURATION
        
        self.state = GameState.RUNNING
        shuffle(MobPopulation)
        shuffle(BossPopulation)

        self.mobs = MobPopulation[:9]
        self.boss.append(BossPopulation[0])

    def expired(self):
        now = time.time()
        return now > self.expireAt
    
        
