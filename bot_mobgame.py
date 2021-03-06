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
MobPopulation = ['zombie', 'hunter', 'brute', 'ettin', 'tank', 'mercenary', 'hacker', 'bulette', 'displacer',
                 'strider', 'kumonga', 'sniper', 'metalpest']

BossPopulation = ['amphisbaena', 'canocephalus', 'mermicolion', 'destoroyah', ]

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
        self.expired()
        return '''\
USAGE
;mox <subcommand or monster> 

subcommands:
  - init            : Start a new game.
  - score           : Show everyone's current scores.
  - list            : List the current mobs that are still alive.

monster:
  - Battles the said monster.
    e.g.  ";mox zombie" will fight the zombie.

RULES:
  When you initiate a game, a set of words will show up,
  with some being harder than the others.
  Type all the words successfully to win the game.
  When playing with more than 2 people,
  you can work together to finish the game,
  or compete against each other for the most points.
'''
    
    def reset(self):
        self.state = GameState.STOPPED
        self.scoreboard = dict()
        self.mobs = []
        self.boss = []
        
    @synchronized
    def setup(self):
        self.expired()
        if self.state == GameState.RUNNING:
            raise Exception("Game is still in progress.")

        # SET UP
        self.reset()
        self.startAt = time.time()
        self.expireAt = time.time() + SEC_EXPIRE_DURATION

        self.state = GameState.RUNNING
        shuffle(MobPopulation)
        shuffle(BossPopulation)

        self.mobs = MobPopulation[:TOTAL_MOBS]
        self.boss.append(BossPopulation[TOTAL_BOSS])
        return self.list()
            
        
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
