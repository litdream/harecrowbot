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
TOTAL_MOBS = 7
TOTAL_BOSS = 1

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
:mox <subcommand> 

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
        self.expired()
        if self.state != GameState.RUNNING:
            self.startAt = time.time()
            self.expireAt = time.time() + SEC_EXPIRE_DURATION

            self.state = GameState.RUNNING
            shuffle(MobPopulation)
            shuffle(BossPopulation)

            self.mobs = MobPopulation[:TOTAL_MOBS]
            self.boss.append(BossPopulation[TOTAL_BOSS])
            return self.list()
            
        else:
            raise Exception("Game is still in progress.")
        
    def expired(self):
        now = time.time()
        if now > self.expireAt:
            self.state = GameState.EXPIRED
            return True
        else:
            return False

    def score(self):
        self.expired()
        sortScore = dict()
        for k in self.scoreboard.keys():
            l = len(self.scoreboard[k])
            if l not in sortScore:
                sortScore[l] = list()
            sortScore[l].append(k)

        lst = []
        for k in reversed(sorted(sortScore.keys())):
            for user in sortScore[k]:
                lst.append("({}) {}: {}".format(k, user, str(self.scoreboard[user])) )
        return '\n'.join(lst)

    
    @synchronized
    def hit(self, user, mobname):
        self.expired()
        if self.state == GameState.RUNNING:
            rtn = ''

            # Currently, mobs and boss are the same.
            #  TODO: Later, split and add more points and dramatic text to BOSS.
            #
            if mobname in self.mobs:
                self.mobs.remove(mobname)
                if user not in self.scoreboard:
                    self.scoreboard[user] = list()
                self.scoreboard[user].append(mobname)
                rtn = "SUCCESS! ( {} )".format(mobname)
            elif mobname in self.boss:
                self.boss.remove(mobname)
                if user not in self.scoreboard:
                    self.scoreboard[user] = list()
                self.scoreboard[user].append(mobname)
                rtn = "SUCCESS! ( {} )".format(mobname)
            else:
                rtn = "No such mob( {} )".format(mobname)

            if len(self.mobs) + len(self.boss) == 0:
                rtn += "\n\nGame Finished.\n"
                rtn += self.score()
                self.state = GameState.STOPPED
                self.expireAt = time.time()
            return rtn
        else:
            raise Exception("Game is not in progress.  Initialize game first.")

    def list(self):
        self.expired()
        if self.state == GameState.RUNNING:
            lst = self.boss + self.mobs
            return "[ {} ]".format(' '.join(lst))
        else:
            return "No mob: Please start game."
