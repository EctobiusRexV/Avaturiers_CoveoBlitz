import game_message
from game_message import *
from actions import *
from random import choice
import math
import numpy as np
from scipy.optimize import fsolve


class Bot:
    shot_meteors = []
    game_message = None

    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")

    def choose_meteor(self):
        target = self.game_message.meteors[0]
        for meteor in self.game_message.meteors:
            valid = True
            for shot_id in self.shot_meteors:
                if meteor.id == shot_id or meteor.position.x < (self.game_message.cannon.position.x + 150):
                    valid = False
            if valid:
                if meteor.meteorType == game_message.MeteorType.Small:
                    return meteor
                elif meteor.meteorType == game_message.MeteorType.Medium:
                    target = meteor if meteor.position.x > target.position.x else target
        return target

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        self.game_message = game_message
        meteor = self.choose_meteor()

        # Système d'équation non linéaire à résoudre
        def func(x):
            return [((game_message.constants.rockets.speed * np.cos(x[0]) - meteor.velocity.x) *
                     x[1] + game_message.cannon.position.x - meteor.position.x),

                    ((game_message.constants.rockets.speed * np.sin(x[0]) - meteor.velocity.y) *
                     x[1] + game_message.cannon.position.y - meteor.position.y)]

        root = fsolve(func, [1, 10])
        if game_message.cannon.cooldown == 0:
            self.shot_meteors.append(meteor.id)
            # for meteor in game_message.meteors:
            #     if meteor.id in self.shot_meteors:
            #         print('\033[92m'+"id:", meteor.id)
            #         print("size:", meteor.meteorType)
            #         print("speed:", meteor.velocity.x, ",", meteor.velocity.y,'\033[0m')
            #     else:
            #         print("id:", meteor.id)
            #         print("size:", meteor.size)
            #         print("speed:", meteor.velocity.x, ",", meteor.velocity.y)
            # print()
            return [
                LookAtAction(target=Vector(meteor.velocity.x * root[1] + meteor.position.x,
                                           meteor.velocity.y * root[1] + meteor.position.y)),
                ShootAction(),
            ]
        else:
            return [
                LookAtAction(target=Vector(meteor.velocity.x * root[1] + meteor.position.x,
                                           meteor.velocity.y * root[1] + meteor.position.y)),
            ]
