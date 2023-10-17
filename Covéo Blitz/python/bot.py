from game_message import *
from actions import *
from random import choice
import math
import numpy as np
from scipy.optimize import fsolve


class Bot:
    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        # cannon = game_message.cannon
        # meteor = choice(game_message.meteors)
        #
        # norme_projectile = game_message.constants.rockets.speed
        # norme_meteor = math.sqrt(meteor.velocity.x ** 2 + meteor.velocity.y ** 2)
        #
        # orientation_meteor = math.arctan(meteor.velocity.y / meteor.velocity.x)

        #Système d'équation non linéaire à résoudre
        def func(x):
            return [((game_message.constants.rockets.speed * np.cos(x[0]) - choice(game_message.meteors).velocity.x) *
                     x[1] + game_message.cannon.position.x - choice(game_message.meteors).position.x),

                    ((game_message.constants.rockets.speed * np.sin(x[0]) - choice(game_message.meteors).velocity.y) *
                     x[1] + game_message.cannon.position.y - choice(game_message.meteors).position.y)]

        root = fsolve(func, [-4, 4])

        return [
            RotateAction(angle=root[0]),
            ShootAction(),
        ]


