import math
import unittest
from src.entities.constants import GOAL_RADIUS, RING_RADIUS, ROBOT_RADIUS
from src.entities.enumerations import Color
from src.entities.mathUtils import Pose2D, distance_between_points
from src.entities.robots import HostRobot, OpposingRobot, PartnerRobot
from src.entities.scoring_elements import BlueGoal, HighNeutralGoal, RedGoal, Ring

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


class TestCollisionsEnabled(unittest.TestCase):
    def test_colliding_rings(self):
        r1 = Ring(Pose2D(0, 0))
        r2 = Ring(Pose2D(0, RING_RADIUS * 0.99))
        
        self.assertTrue(r1.is_colliding(r2))
        self.assertTrue(r2.is_colliding(r1))

    def test_colliding_goals(self):
        g1 = RedGoal(Pose2D(0, 0))
        g2 = BlueGoal(Pose2D(GOAL_RADIUS * 0.5, GOAL_RADIUS * 0.5))
        
        self.assertTrue(g1.is_colliding(g2))
        self.assertTrue(g2.is_colliding(g1))

    def test_colliding_robots(self):
        r1 = PartnerRobot(Color.RED, Pose2D(0, 0))
        r2 = OpposingRobot(Color.BLUE, Pose2D(-ROBOT_RADIUS * 0.5, -ROBOT_RADIUS * 0.3))

        self.assertTrue(r1.is_colliding(r2))
        self.assertTrue(r2.is_colliding(r1))

    def test_goal_ring_colliding(self):
        r1 = Ring(Pose2D(0, 0))
        g1 = HighNeutralGoal(Pose2D(0, GOAL_RADIUS * 0.99))

        self.assertTrue(r1.is_colliding(g1))
        self.assertTrue(g1.is_colliding(r1))

    def test_multi_colliding(self):
        ring = Ring(Pose2D(0, 0))
        goal = HighNeutralGoal(Pose2D(0, GOAL_RADIUS * 0.99))
        robot = HostRobot(Color.RED, Pose2D(ROBOT_RADIUS * 0.99, 0))

        # The ring and goal overlap
        self.assertTrue(ring.is_colliding(goal))
        self.assertTrue(goal.is_colliding(ring))

        # The ring and robot overlap
        self.assertTrue(ring.is_colliding(robot))
        self.assertTrue(robot.is_colliding(ring))

        # The goal and robot do not overlap
        self.assertFalse(robot.is_colliding(goal))
        self.assertFalse(goal.is_colliding(robot))

    def test_not_colliding(self):
        r1 = Ring(Pose2D(0, 0))
        g1 = HighNeutralGoal(Pose2D(0, GOAL_RADIUS * 1.01))

        self.assertFalse(r1.is_colliding(g1))
        self.assertFalse(g1.is_colliding(r1))


if __name__ == "__main__":
    unittest.main()