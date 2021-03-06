import os
import time
import random
from enum import Enum
from bot_mobgame import GameState, synchronized


MAX_GAME_DURATION = 60 * 5    # 5 minutes
MAX_CHANCE = 7

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
  - init        : Start a new game.
  - status      : Show each user's current game history.
  - help        : Look at what each of the game's subcommands do.

guess-number:
  - 3 digit of your number to match
    e.g. ";num 321"

REMEMBER:  You have total of {} chances!  Guess based on clues you collect.

RULES:
  When you initiate a game, you will be met with a challenge to guess a 3 digit number.
  This 3 digit number has different digits.  For example, '467', but not '366'.
  Each player has 7 chances. Each time you guess, a small text box will appear to the right of your number.
  If a digit is there, and it's in the right place, it will be counted as an 's'.
  A "b" means that there is a digit that is in the number, but in the wrong place. (Example: 1b 0s)
  Your goal is to get three s's, which is the exact number the bot thought.
  If everyone run out of chances, everyone loses.
  If one player guesses the number correctly, that player wins.
'''.format(MAX_CHANCE)
    
    
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
        return "Okay, I have a 3 digit number. Guess it!"
    
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
        if toUser not in self.uHistory:
            self.uHistory[toUser] = list()
        if self.state != GameState.RUNNING:
            Exception("Game is not running. Please start a new game with ';num init'.")
        if len( set(uNum)) < 3:
            raise Exception("No repeating digits, please. Each digit should be unique.")
        if len( self.uHistory[toUser] ) >= MAX_CHANCE:
            raise Exception("You ran out of all {} chances.".format(MAX_CHANCE))
        
        # Early exit for matching number
        if uNum == self.num:
            return 3, "{}(0b 3s)".format(uNum)

        # If not matching, count strike/ball, and chances.
        strike, ball = 0,0
        # For strikes
        for i in (0,1,2):
            if self.num[i] == uNum[i]:
                strike += 1
        # For balls
        if uNum[0] == self.num[1] or uNum[0] == self.num[2]:
                ball += 1
        if uNum[1] == self.num[0] or uNum[1] == self.num[2]:
                ball += 1
        if uNum[2] == self.num[0] or uNum[2] == self.num[1]:
                ball += 1
        elm = "{}({}b {}s)".format(uNum, ball, strike)
        self.uHistory[toUser].append(elm)

        # See if everyone ran out of chances.
        tot_chances = len(self.uHistory) * MAX_CHANCE
        cur_chances = 0
        for k,v in self.uHistory.items():
            cur_chances += len(v)

        if cur_chances >= tot_chances:
            self.expireAt = time.time()
            self.state = GameState.STOPPED
            raise Exception("Hahaha! I won!! You all ran out of chances.  My number was {}.".format(self.num))

        # Finally, check if this person ran out of chance.
        msg = elm + "  : {} chances left.".format( MAX_CHANCE - len(self.uHistory[toUser]))
        return strike, msg

        # This is for when time runs out.
        