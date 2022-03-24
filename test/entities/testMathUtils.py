import unittest
from src.entities.mathUtils import Pose2D, distance_between_points

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
        self.assertTrue(False)


class TestDistanceBetweenPoints(unittest.TestCase):
    def test_distance_between_points(self):
        poseA = Pose2D(5, 10)
        poseB = Pose2D(10, 10)

        dist = distance_between_points(poseA, poseB)

        self.assertEqual(dist, 5)


if __name__ == "__main__":
    unittest.main()