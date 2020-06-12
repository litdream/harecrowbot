import os
import random

class Laugh:
    def __init__(self, ctx):
        self.ctx = ctx

    def laugh(self):
        lst = [
            'https://giphy.com/gifs/laughing-spider-man-j-jonah-jameson-dC9DTdqPmRnlS',
            'https://giphy.com/gifs/disney-cartoon-laughing-ECtLJKdGj8jfy',
            'https://giphy.com/gifs/laughing-joker-jack-nicholson-tMyCJmeXHBetq',
            'https://giphy.com/gifs/swPH6f77yLk2I',
            'https://giphy.com/gifs/laughing-duck-donald-Mjl0BsAgMGYTe',
            'https://giphy.com/gifs/laughing-despicable-me-minions-ZqlvCTNHpqrio',
            'https://giphy.com/gifs/bbc-bbc-three-big-narstie-lets-settle-this-9AIelkWMWzU2Yivx8V',
            'https://giphy.com/gifs/laughing-laugh-gE6IUBRWZd744',
            'https://giphy.com/gifs/laughing-cristiano-ronaldo-LBA8IfDSb7TBS',
        ]
        random.shuffle(lst)
        return lst[0]
