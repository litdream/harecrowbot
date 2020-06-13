import os
import time
import random
from enum import Enum
from bot_mobgame import GameState, synchronized


MAX_GAME_DURATION = 60 * 5    # 5 minutes

class Numgame:
    def __init__(self):
        self.startAt =0
        self.expireAt =0
        self.pop = list('123456789')
        self.reset()

    def help(self):
        self.expired()
        return '''\
USAGE
;num <subcommand or guess-number>

subcommand:
  - init        : initialize a new game
  - status      : show status for the game

guess-number:
  - 3 digit of your number to match
    e.g. ";num 321"

REMEMBER:  You have total of 7 chances!  Guess based on clues you collect.

'''
    
    def reset(self):
        self.state = GameState.STOPPED
        self.uHistory = dict()
        random.shuffle(self.pop)
        self.num = ''.join( self.pop[:3])

    @synchronized
    def setup(self):
        self.expired()
        if self.state == GameState.RUNNING:
            raise Exception("Game is still in progress.")
        
        self.reset()
        self.state = GameState.RUNNING
        self.startAt = time.time()
        self.expireAt = self.startAt + MAX_GAME_DURATION
        
    def expired(self):
        now = time.time()
        if now > self.expireAt:
            self.state = GameState.EXPIRED
            return True
        else:
            return False
        
    def status(self):
        self.expired()
        rtn = list()
        for u,hist in self.uHistory.items():
            rtn.append('{}: {}'.format(u, ' '.join(hist)) )
        return '\n'.join(rtn)

    def match(self, toUser, uNum):
        self.expired()
        # sanity check
        if self.state != GameState.RUNNING:
            Exception("Game is not running.  Please init ';num init'.")
            
        if len( set(uNum)) < 3:
            raise Exception("No repeating digit, please.  Each digit should be unique.")

        if toUser not in self.uHistory:
            self.uHistory[toUser] = list()
        if len( self.uHistory[toUser] ) >= 7:
            raise Exception("You ran out of all 7 chances.")
            
        strike = 0
        for i in (0,1,2):
            if self.num[i] == uNum[i]:
                strike += 1

        ball = 0
        if uNum[0] == self.num[1] or uNum[0] == self.num[2]:
                ball += 1
        if uNum[1] == self.num[0] or uNum[1] == self.num[2]:
                ball += 1
        if uNum[2] == self.num[0] or uNum[2] == self.num[1]:
                ball += 1

        elm = "{}({}b {}s)".format(uNum, ball, strike)
        self.uHistory[toUser].append(elm)
        
        return strike, elm
        
    
