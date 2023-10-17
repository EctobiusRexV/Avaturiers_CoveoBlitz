from game_message import *
from actions import *
from random import choice
import math
import numpy


class Bot:
    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        cannon = game_message.cannon
        meteor = choice(game_message.meteors)

        norme_projectile = game_message.constants.rockets.speed
        norme_meteor = math.sqrt(meteor.velocity.x**2 + meteor.velocity.y**2)

        orientation_meteor = math.arctan(meteor.velocity.y / meteor.velocity.x)



        return [
            LookAtAction(target=Vector()),
            ShootAction(),
        ]
