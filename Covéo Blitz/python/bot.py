from game_message import *
from actions import *
import math
import numpy as np
from scipy.optimize import fsolve


def calculate_future_position(game_message: GameMessage, meteor: Meteor):
    """
    Calculates when and where the meteor would collide with the bullet if the bot shot it at this game state
    :param game_message: The game state
    :param meteor: The meteor that would be shot
    :return: A tuple with the first element being the angle of the cannon and the second one being the time until the collision happens
    """
    def func(x):
        return [((game_message.constants.rockets.speed * np.cos(x[0]) - meteor.velocity.x) *
                 x[1] + game_message.cannon.position.x - meteor.position.x),

                ((game_message.constants.rockets.speed * np.sin(x[0]) - meteor.velocity.y) *
                 x[1] + game_message.cannon.position.y - meteor.position.y)]
    return fsolve(func, [1, 10])


def meteor_in_shootable_range(angle: float, position: Vector) -> bool:
    """
    Evaluates whether a position is within the shootable range of the gun
    :param angle: The angle of the shot
    :param position: The predicted position of the meteor
    :return: Whether we should shoot the meteor or not
    """
    return (10 < position.y < 790) and (-math.pi * 0.45 < angle < math.pi * 0.45)


class Bot:
    shot_meteors = []
    predicted_meteors = []

    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")

    def choose_meteor(self, game_message: GameMessage) -> Meteor:
        """
        Chooses the best meteor to shoot on the map
        :param game_message: The game message containing the meteors
        :return: The chosen meteor
        """
        if len(game_message.meteors) == 0:
            return None
        target = game_message.meteors[0]
        for meteor in game_message.meteors:
            valid = True
            for shot_id in self.shot_meteors:
                if meteor.id == shot_id:
                    valid = False
            if valid:
                if meteor.meteorType == MeteorType.Small:
                    return meteor
                elif meteor.meteorType == MeteorType.Medium:
                    target = meteor
                if meteor.meteorType == target.meteorType and meteor.position.x > target.position.x:
                    target = meteor
        return target

    def predict_meteors(self, meteor, time) -> None:
        """
        Creates fake meteors at spots where they are predicted to be when the passed in meteor is destroyed
        :param meteor: The meteor that has just been shot but not yet destroyed
        :param time: The time it will take for the meteor to be destroyed
        """
        impact_position = Vector(x=meteor.velocity.x * time + meteor.position.x,
                                 y=meteor.velocity.y * time + meteor.position.y)
        main_angle = math.atan2(meteor.velocity.y, meteor.velocity.x)
        if meteor.meteorType == MeteorType.Large:
            for angle in [main_angle + math.pi / 10, main_angle - math.pi / 10]:
                predict_id = "0" if len(self.predicted_meteors) == 0 else str(int(self.predicted_meteors[-1].id) + 1)
                velocity = Vector(x=8 * math.cos(angle), y=8 * math.sin(angle))
                position = Vector(x=impact_position.x - velocity.x * time, y=impact_position.y - velocity.y * time)
                self.predicted_meteors.append(
                    Meteor(id=predict_id, position=position, velocity=velocity, size=math.ceil(time),
                           meteorType=MeteorType.Medium))
        elif meteor.meteorType.Medium:
            for angle in [main_angle + math.pi / 6, main_angle, main_angle - math.pi / 6]:
                predict_id = "0" if len(self.predicted_meteors) == 0 else str(int(self.predicted_meteors[-1].id) + 1)
                velocity = Vector(x=13 * math.cos(angle), y=13 * math.sin(angle))
                position = Vector(x=impact_position.x - velocity.x * time, y=impact_position.y - velocity.y * time)
                self.predicted_meteors.append(
                    Meteor(id=predict_id, position=position, velocity=velocity, size=math.ceil(time),
                           meteorType=MeteorType.Small))

    def update_predicted_meteors(self, game_message: GameMessage) -> None:
        """
        Updates the position of the predicted meteors according to their predicted velocity
        :param game_message: Current game message
        """
        for meteor in self.predicted_meteors:
            meteor.position.x += meteor.velocity.x
            meteor.position.y += meteor.velocity.y
            meteor.size -= 1
            if meteor.size == 0:
                if meteor.id in self.shot_meteors:
                    self.shot_meteors.remove(meteor.id)
                    for real_meteor in game_message.meteors:
                        if math.isclose(real_meteor.velocity.x, meteor.velocity.x, abs_tol=1.0) and math.isclose(
                                real_meteor.velocity.y, meteor.velocity.y, abs_tol=1.0):
                            self.shot_meteors.append(real_meteor.id)
                self.predicted_meteors.remove(meteor)
        game_message.meteors.extend(self.predicted_meteors)

    def should_predict_meteor(self, meteor: Meteor):
        """
        Evaluate whether we should attempt to predict the smaller meteors that will result from shooting a meteor
        :param meteor: The meteor that got shot
        :return: Whether we should shoot the meteor
        """
        return meteor.meteorType == MeteorType.Large and meteor.id not in self.shot_meteors

    def get_next_move(self, game_message: GameMessage):
        """
        Gets called every tick and decides what action the bot should make
        :param game_message: An object containing all the data we get from the server
        :return: The actions we will take this tick
        """
        self.update_predicted_meteors(game_message)
        meteor = self.choose_meteor(game_message)
        if meteor is None:
            return []

        if game_message.cannon.cooldown == 0:
            root = calculate_future_position(game_message, meteor)
            target = Vector(meteor.velocity.x * root[1] + meteor.position.x, meteor.velocity.y * root[1] + meteor.position.y)
            i = 0
            while not meteor_in_shootable_range(root[0], target):
                if i > len(game_message.meteors):
                    print(game_message.tick)
                    return []
                self.shot_meteors.append(meteor.id)
                root = calculate_future_position(game_message, meteor)
                target = Vector(meteor.velocity.x * root[1] + meteor.position.x, meteor.velocity.y * root[1] + meteor.position.y)
                i += 1
            if self.should_predict_meteor(meteor):
                self.predict_meteors(meteor, root[1])
            self.shot_meteors.append(meteor.id)
            return [
                LookAtAction(target=target),
                ShootAction(),
            ]
        else:
            return []