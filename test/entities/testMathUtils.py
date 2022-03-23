import math
import unittest
from src.entities.mathUtils import Pose2D, distance_between_points
from src.entities.robots import OpposingRobot
from src.entities.scoring_elements import Ring

class TestPose2D(unittest.TestCase):
    def test_initialization(self):
        pose = Pose2D(10, 20)

        self.assertEqual(pose.x, 10)
        self.assertEqual(pose.y, 20)

    def test_dist_to_point(self):
        poseA = Pose2D(5, 10)
        poseB = Pose2D(10, 10)

        self.assertEqual(poseA.distTo(poseB), 5)
        self.assertEqual(poseB.distTo(poseA), 5)


class TestDistanceBetweenPoints(unittest.TestCase):
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