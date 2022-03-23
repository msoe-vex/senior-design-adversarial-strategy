import unittest
from src.entities.mathUtils import Pose2D, distance_between_points
from src.entities.robots import OpposingRobot
from src.entities.scoring_elements import Ring
import math

class TestMathUtils(unittest.TestCase):
    def test_pose2d(self):
        self.assertTrue(True)

    def test_distance_between_points(self):
        p1 = Pose2D(-5, 2)
        p2 = Pose2D(3, 4)
        self.assertEqual(math.sqrt(68), distance_between_points(p1, p2))

    def test_is_colliding(self):
        rob = OpposingRobot(Pose2D(-5, 2))
        ring = Ring(Pose2D(3, 4))
        col = rob.is_colliding(ring)
        self.assertTrue(col)



if __name__ == "__main__":
    unittest.main()