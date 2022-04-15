import math
import unittest
from src.entities.constants import GOAL_RADIUS, RING_RADIUS, ROBOT_RADIUS
from src.entities.enumerations import Color
from src.entities.mathUtils import Pose2D, distance_between_points, distance_between_entities, vector_rotate
from src.entities.robots import HostRobot, OpposingRobot, PartnerRobot
from src.entities.scoring_elements import BlueGoal, HighNeutralGoal, RedGoal, Ring

class TestPose2D(unittest.TestCase):
    def test_initialization(self):
        pose = Pose2D(10, 20, 0)

        self.assertEqual(pose.x, 10, 0)
        self.assertEqual(pose.y, 20, 0)

    def test_dist_to_point(self):
        poseA = Pose2D(5, 10, 0)
        poseB = Pose2D(10, 10, 0)

        self.assertEqual(poseA.distTo(poseB), 5, 0)
        self.assertEqual(poseB.distTo(poseA), 5, 0)


class TestVectorRotate(unittest.TestCase):
    def test_rotate_0(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate(0, a)
        expected_b = Pose2D(1, 0, 0)

        self.assertEqual(b, expected_b)

    def test_rotate_45(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate(math.pi / 4, a)
        expected_b = Pose2D(math.sqrt(0.5), math.sqrt(0.5), 0)

        c = vector_rotate(-math.pi / 4, a)
        expected_c = Pose2D(math.sqrt(0.5), -math.sqrt(0.5), 0)

        self.assertEqual(b, expected_b)
        self.assertEqual(c, expected_c)

    def test_rotate_90(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate(math.pi / 2, a)
        expected_b = Pose2D(0, 1, 0)

        c = vector_rotate(-math.pi / 2, a)
        expected_c = Pose2D(0, -1, 0)

        self.assertEqual(b, expected_b)
        self.assertEqual(c, expected_c)

    def test_rotate_180(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate(math.pi, a)
        expected_b = Pose2D(-1, 0, 0)

        c = vector_rotate(-math.pi, a)
        expected_c = Pose2D(-1, 0, 0)

        self.assertEqual(b, expected_b)
        self.assertEqual(c, expected_c)

    def test_rotate_270(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate((3 * math.pi) / 2, a)
        expected_b = Pose2D(0, -1, 0)

        c = vector_rotate(-(3 * math.pi) / 2, a)
        expected_c = Pose2D(0, 1, 0)

        self.assertEqual(b, expected_b)
        self.assertEqual(c, expected_c)

    def test_rotate_360(self):
        a = Pose2D(1, 0, 0)

        b = vector_rotate((2 * math.pi), a)
        expected_b = Pose2D(1, 0, 0)

        c = vector_rotate((2 * math.pi), a)
        expected_c = Pose2D(1, 0, 0)

        self.assertEqual(b, expected_b)
        self.assertEqual(c, expected_c)


class TestDistanceBetweenPoints(unittest.TestCase):
    def test_distance_between_points(self):
        p1 = Pose2D(-5, 2, 0)
        p2 = Pose2D(3, 4, 0)
        self.assertEqual(math.sqrt(68), distance_between_points(p1, p2))


class TestCollisionsEnabled(unittest.TestCase):
    def test_colliding_rings(self):
        r1 = Ring(Pose2D(0, 0, (math.pi / 2)))
        r2 = Ring(Pose2D(0, RING_RADIUS, 0))
        r3 = Ring(Pose2D(0, -RING_RADIUS, 0))
        r4 = Ring(Pose2D(RING_RADIUS, 0, 0))
        
        # General collision
        self.assertTrue(r1.is_colliding(r2))
        self.assertTrue(r2.is_colliding(r1))

        self.assertTrue(r1.is_colliding(r3))
        self.assertTrue(r3.is_colliding(r1))

        self.assertTrue(r1.is_colliding(r4))
        self.assertTrue(r4.is_colliding(r1))

        # Front collision
        self.assertTrue(r1.is_colliding_front(r2))

        # Rear collision
        self.assertTrue(r1.is_colliding_rear(r3))

        # Left collision
        self.assertFalse(r1.is_colliding_front(r4))
        self.assertFalse(r1.is_colliding_rear(r4))

    def test_colliding_goals(self):
        g1 = RedGoal(Pose2D(0, 0, (math.pi / 2)))
        g2 = BlueGoal(Pose2D(GOAL_RADIUS * 0.5, GOAL_RADIUS * 0.5, 0))
        g3 = RedGoal(Pose2D(0, GOAL_RADIUS, 0))
        g4 = RedGoal(Pose2D(0, -GOAL_RADIUS, 0))
        g5 = RedGoal(Pose2D(GOAL_RADIUS, 0, 0))
        
        # General collision
        self.assertTrue(g1.is_colliding(g2))
        self.assertTrue(g2.is_colliding(g1))

        self.assertTrue(g1.is_colliding(g3))
        self.assertTrue(g3.is_colliding(g1))

        self.assertTrue(g1.is_colliding(g4))
        self.assertTrue(g4.is_colliding(g1))

        self.assertTrue(g1.is_colliding(g5))
        self.assertTrue(g5.is_colliding(g1))

        # Front collision
        self.assertTrue(g1.is_colliding_front(g3))

        # Rear collision
        self.assertTrue(g1.is_colliding_rear(g4))

        # Left collision
        self.assertFalse(g1.is_colliding_front(g5))
        self.assertFalse(g1.is_colliding_rear(g5))

    def test_colliding_robots(self):
        r1 = PartnerRobot(Color.RED, Pose2D(0, 0, (math.pi / 2)))
        r2 = OpposingRobot(Color.BLUE, Pose2D(-ROBOT_RADIUS * 0.5, -ROBOT_RADIUS * 0.3, 0))
        r3 = PartnerRobot(Color.RED, Pose2D(0, ROBOT_RADIUS, 0))
        r4 = PartnerRobot(Color.RED, Pose2D(0, -ROBOT_RADIUS, 0))
        r5 = PartnerRobot(Color.RED, Pose2D(ROBOT_RADIUS, 0, 0))

        # General collision
        self.assertTrue(r1.is_colliding(r2))
        self.assertTrue(r2.is_colliding(r1))

        self.assertTrue(r1.is_colliding(r3))
        self.assertTrue(r3.is_colliding(r1))

        self.assertTrue(r1.is_colliding(r4))
        self.assertTrue(r4.is_colliding(r1))

        self.assertTrue(r1.is_colliding(r5))
        self.assertTrue(r5.is_colliding(r1))

        # Front collision
        self.assertTrue(r1.is_colliding_front(r3))

        # Rear collision
        self.assertTrue(r1.is_colliding_rear(r4))

        # Left collision
        self.assertFalse(r1.is_colliding_front(r5))
        self.assertFalse(r1.is_colliding_rear(r5))

    def test_goal_ring_colliding(self):
        r1 = Ring(Pose2D(0, 0, 0))
        g1 = HighNeutralGoal(Pose2D(0, GOAL_RADIUS, 0))

        self.assertTrue(r1.is_colliding(g1))
        self.assertTrue(g1.is_colliding(r1))

    def test_multi_colliding(self):
        ring = Ring(Pose2D(0, 0, 0))
        goal = HighNeutralGoal(Pose2D(0, GOAL_RADIUS, 0))
        robot = HostRobot(Color.RED, Pose2D(ROBOT_RADIUS, 0, 0))

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
        r1 = Ring(Pose2D(0, 0, 0))
        g1 = HighNeutralGoal(Pose2D(0, GOAL_RADIUS * 1.01, 0))

        self.assertFalse(r1.is_colliding(g1))
        self.assertFalse(g1.is_colliding(r1))


class TestDistanceBetweenEntities(unittest.TestCase):
    def test_distance_between_entities(self):
        ent1 = Ring(Pose2D(0, 1))
        ent2 = HostRobot(Color.BLUE, Pose2D(ROBOT_RADIUS + 8, 1))

        dist = distance_between_entities(ent1, ent2)
        self.assertEqual(dist, 6)

    def test_distance_between_collding(self):
        g1 = RedGoal(Pose2D(0, 0))
        g2 = BlueGoal(Pose2D(GOAL_RADIUS * 0.5, GOAL_RADIUS * 0.5))

        dist = distance_between_entities(g1, g2)
        self.assertEqual(dist, 0)


if __name__ == "__main__":
    unittest.main()