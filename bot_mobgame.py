import os
import time
from enum import Enum
from random import shuffle
import threading

'''
Simple statemachine for mobgame.

Unlike simple methods, Mobgame will raise Exceptions.
Handle exception in the 'bot.py' command entry.

'''
class GameState(Enum):
    STOPPED = 1
    RUNNING = 2
    EXPIRED = 3

SEC_EXPIRE_DURATION = 3 * 60    # 3 minutes

# To be adjusted: Jake is working on it.
MobPopulation = ['zombie', 'dwarf', 'brute', 'ettin', 'frog', 'earthworm', 'rabbit', 'buffalo', 'gnome', 'kraken' ]
BossPopulation = ['amphisbaena', 'canocephalus', 'mermicolion']

def synchronized(func):
    func.__lock__ = threading.Lock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func

class Mobgame:
    def __init__(self):
        self.reset()
        self.startAt = 0
        self.expireAt = 0

    def help(self):
        return '''\
USAGE
:mob <subcommand> 

subcommands:
  - init            : initialize a new game
  - score           : print current scoreboard
  - hit <mobname>   : fight with mob.
  - list            : list current mobs
'''
    
    def reset(self):
        self.state = GameState.STOPPED
        self.scoreboard = dict()
        self.mobs = []
        self.boss = []
        
    @synchronized
    def setup(self):
        if self.state != GameState.RUNNING:
            self.startAt = time.time()
            self.expireAt = time.time() + SEC_EXPIRE_DURATION

            self.state = GameState.RUNNING
            shuffle(MobPopulation)
            shuffle(BossPopulation)

            self.mobs = MobPopulation[:7]
            self.boss.append(BossPopulation[0])
        else:
            raise Exception("Game is still in progress.")
        
    def expired(self):
        now = time.time()
        if now > self.expireAt:
            self.state = GameState.EXPIRED
            return True
        else:
            return False
            
    @synchronized
    def hit(self, user, mobname):
        pass
        
