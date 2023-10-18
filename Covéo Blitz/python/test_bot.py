import math
from unittest import TestCase
from bot import Bot
from game_message import GameMessage
from game_message import Meteor
from game_message import Projectile
from game_message import MeteorType
from game_message import Vector


class TestBot(TestCase):
    def test_choose_meteor(self):
        bot = Bot()
        meteors = [Meteor(id='3685', position=Vector(x=980.2300569238887, y=257.5607603575879),
                          velocity=Vector(x=-7.966004299873837, y=-2.4957069619393892), size=20.0,
                          meteorType=MeteorType.Medium),
                   Meteor(id='3687', position=Vector(x=952.0306547483968, y=371.16409826240056),
                          velocity=Vector(x=-9.188905997322188, y=10.42441923512799), size=5.0,
                          meteorType=MeteorType.Small),
                   Meteor(id='3688', position=Vector(x=940.4149225393088, y=323.7557926430601),
                          velocity=Vector(x=-10.848296312906207, y=3.6518041466507487), size=5.0,
                          meteorType=MeteorType.Small),
                   Meteor(id='3689', position=Vector(x=942.9944110940967, y=283.40747721975947),
                          velocity=Vector(x=-10.479797947936452, y=-2.1122409138207687), size=5.0,
                          meteorType=MeteorType.Small),
                   Meteor(id='3690', position=Vector(x=1242.5282986330337, y=557.5065108439812),
                          velocity=Vector(x=-2.490567122322131, y=0.05464889310075238), size=40.0,
                          meteorType=MeteorType.Large)]

        game_message = GameMessage(type='test', tick=0, lastTickErrors=[""], constants=None, cannon=None,
                                   meteors=meteors, rockets=[None], score=0)
        bot.game_message = game_message
        self.assertEqual(MeteorType.Small, bot.choose_meteor().meteorType)

    def test_predict_meteors(self):
        bot = Bot()
        meteor = Meteor(id='3685', position=Vector(x=1000, y=250),
                        velocity=Vector(x=-8, y=-2.5), size=40.0,
                        meteorType=MeteorType.Large)
        bot.predict_meteors(meteor, 45)
        self.assertTrue(math.isclose(-6.5247, bot.predicted_meteors[0].velocity.x, abs_tol=0.01))
        self.assertTrue(math.isclose(-4.6290, bot.predicted_meteors[0].velocity.y, abs_tol=0.01))
        self.assertTrue(math.isclose((1000-8*45)-(-6.5247*45), bot.predicted_meteors[0].position.x, abs_tol=0.01))
        self.assertTrue(math.isclose((250-2.5*45)-(-4.6290*45), bot.predicted_meteors[0].position.y, abs_tol=0.01))
