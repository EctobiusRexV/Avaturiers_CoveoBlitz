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
        #meteor = meteor
        #
        # norme_projectile = game_message.constants.rockets.speed
        # norme_meteor = math.sqrt(meteor.velocity.x ** 2 + meteor.velocity.y ** 2)
        #
        # orientation_meteor = math.arctan(meteor.velocity.y / meteor.velocity.x)
        meteor = choice(game_message.meteors)
        #Système d'équation non linéaire à résoudre
        def func(x):
            return [((game_message.constants.rockets.speed * np.cos(x[0]) - meteor.velocity.x) *
                     x[1] + game_message.cannon.position.x - meteor.position.x),

                    ((game_message.constants.rockets.speed * np.sin(x[0]) - meteor.velocity.y) *
                     x[1] + game_message.cannon.position.y - meteor.position.y)]

        root = fsolve(func, [1, 10])
        print("Meteor position", game_message.meteors[0].position)
        print("Meteor velocity", game_message.meteors[0].velocity)
        print("Cannon position", game_message.cannon.position)
        print("Cannon initial velocity", game_message.constants.rockets.speed)
        print("Roots", root)
        # if game_message.cannon.cooldown == 0:
        return [
                #LookAtAction(target=Vector(game_message.meteors[0].position.x, game_message.meteors[0].position.y)),
                LookAtAction(target=Vector(meteor.velocity.x*root[1]+meteor.position.x, meteor.velocity.y*root[1]+meteor.position.y)),
                ShootAction(),
            ]
        # else:
        #     return [
        #         LookAtAction(target=Vector(meteor.velocity.x*root[1]+meteor.position.x, meteor.velocity.y*root[1]+meteor.position.y)),
        #         #LookAtAction(target=Vector(game_message.meteors[0].position.x, game_message.meteors[0].position.y)),
        #     ]





