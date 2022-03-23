from __future__ import annotations
import json
from logging import getLogger
import random
from cv2 import idct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Tuple
from dataclasses import field
from entities.classUtils import nested_dataclass
from entities.constants import *
from entities.enumerations import Color, convertColorToRGBA
from entities.interfaces import ISerializable
from entities.mathUtils import Pose2D
from entities.platforms import PlatformState, RedPlatform, BluePlatform
from entities.scoring_elements import (
    BlueGoal,
    GoalLevel,
    Goal,
    HighNeutralGoal,
    LowNeutralGoal,
    RedGoal,
    Ring,
)
from entities.robots import HostRobot, OpposingRobot, PartnerRobot, Robot


@nested_dataclass
class FieldCounts:
    red_goals: int = 0
    max_red_goals: int = MAX_NUM_RED_GOALS
    blue_goals: int = 0
    max_blue_goals: int = MAX_NUM_BLUE_GOALS
    low_neutral_goals: int = 0
    max_low_neutral_goals: int = MAX_NUM_LOW_NEUTRAL_GOALS
    high_neutral_goals: int = 0
    max_high_neutral_goals: int = MAX_NUM_HIGH_NEUTRAL_GOALS
    rings: int = 0
    max_rings: int = MAX_NUM_RINGS
    host_robots: int = 0
    max_host_robots: int = MAX_NUM_HOST_ROBOTS
    partner_robots: int = 0
    max_partner_robots: int = MAX_NUM_PARTNER_ROBOTS
    opposing_robots: int = 0
    max_opposing_robots: int = MAX_NUM_OPPOSING_ROBOTS

    def get_remaining_red_goals(self) -> int:
        remaining = self.max_red_goals - self.red_goals

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining red goals is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_blue_goals(self) -> int:
        remaining = self.max_blue_goals - self.blue_goals

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining blue goals is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_low_neutral_goals(self) -> int:
        remaining = self.max_low_neutral_goals - self.low_neutral_goals

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining low neutral goals is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_high_neutral_goals(self) -> int:
        remaining = self.max_high_neutral_goals - self.high_neutral_goals

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining high neutral goals is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_goals(self) -> int:
        remaining = self.get_remaining_red_goals()
        remaining += self.get_remaining_blue_goals()
        remaining += self.get_remaining_low_neutral_goals()
        remaining += self.get_remaining_high_neutral_goals()

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Total remaining goals is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_rings(self) -> int:
        remaining = self.max_rings - self.rings

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining rings is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_host_robots(self) -> int:
        remaining = self.max_host_robots - self.host_robots

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining host robots is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_partner_robots(self) -> int:
        remaining = self.max_partner_robots - self.partner_robots

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining partner robots is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_opposing_robots(self) -> int:
        remaining = self.max_opposing_robots - self.opposing_robots

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Remaining opposing robots is less than zero ({remaining})"
            )

        return remaining

    def get_remaining_robots(self) -> int:
        remaining = self.get_remaining_host_robots()
        remaining += self.get_remaining_partner_robots()
        remaining += self.get_remaining_opposing_robots()

        if remaining < 0:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Total remaining robots is less than zero ({remaining})"
            )

        return remaining


@nested_dataclass
class FieldRepresentation(ISerializable):
    red_platform: RedPlatform = RedPlatform(PlatformState.LEVEL)
    blue_platform: BluePlatform = BluePlatform(PlatformState.LEVEL)
    rings: list[Ring] = field(default_factory=list)
    goals: list[Goal] = field(default_factory=list)
    robots: list[Robot] = field(default_factory=list)
    field_counts: FieldCounts = FieldCounts()

    def __get_alliance_color(
        self, random_color: int, host_alliance: bool = True
    ) -> Color:
        if host_alliance:
            return Color.RED if random_color == 0 else Color.BLUE
        return Color.BLUE if random_color == 0 else Color.RED

    def __generate_ring_list(
        self, pose: Pose2D, percentage: float, discount: float, current_iter: int = 0
    ) -> list[Ring]:
        self.field_counts.rings += 1

        if (
            percentage < (percentage * ((current_iter + 1) * discount))
            and self.field_counts.get_remaining_rings() > 1
        ):
            return [Ring(pose)] + self.__generate_ring_list(
                pose, percentage, discount, current_iter + 1
            )
        else:
            return [Ring(pose)]

    def __add_rings_to_goal(self, goal: Goal) -> None:
        percent = random.random()

        rings = self.__generate_ring_list(
            goal.pose, SPAWN_RING_ON_GOAL, ADDITIONAL_RING_ON_GOAL_DISCOUNT_FACTOR
        )

        getLogger(REPRESENTATION_LOGGER_NAME).info(
            f"Spawned {len(rings)} rings on {type(goal).__name__} goal at ({goal.pose.x},{goal.pose.y})"
        )

        for ring in rings:
            if (
                percent < SPAWN_RING_ON_HIGH_BRANCH
                and goal.get_ring_container(GoalLevel.HIGH).get_remaining_utilization()
                > 0
            ):
                goal.get_ring_container(GoalLevel.HIGH).add_ring(ring)
            elif (
                percent < SPAWN_RING_ON_LOW_BRANCH
                and goal.get_ring_container(GoalLevel.LOW).get_remaining_utilization()
                > 0
            ):
                goal.get_ring_container(GoalLevel.LOW).add_ring(ring)
            elif (
                goal.get_ring_container(GoalLevel.BASE).get_remaining_utilization() > 0
            ):
                goal.get_ring_container(GoalLevel.BASE).add_ring(ring)

    def __generate_goal_list(
        self, pose: Pose2D, percentage: float, discount: float, current_iter: int = 0
    ) -> list[Goal]:
        goal_num = random.randint(0, 3)

        goal = None
        if goal_num == 0 and self.field_counts.get_remaining_low_neutral_goals() > 0:
            goal = LowNeutralGoal(pose)
            self.field_counts.low_neutral_goals += 1
        elif goal_num == 1 and self.field_counts.get_remaining_high_neutral_goals() > 0:
            goal = HighNeutralGoal(pose)
            self.field_counts.high_neutral_goals += 1
        elif goal_num == 2 and self.field_counts.get_remaining_red_goals() > 0:
            goal = RedGoal(pose)
            self.field_counts.red_goals += 1
        elif self.field_counts.get_remaining_blue_goals() > 0:
            goal = BlueGoal(pose)
            self.field_counts.blue_goals += 1
        else:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Attempting to spawn goal of number {goal_num} when all goals are spawned"
            )

        if goal is not None:
            getLogger(REPRESENTATION_LOGGER_NAME).info(
                f"Spawned {type(goal).__name__} at ({pose.x},{pose.y})"
            )

            if random.random() < SPAWN_RING_ON_GOAL:
                self.__add_rings_to_goal(goal)

            if (
                percentage < (percentage * ((current_iter + 1) * discount))
                and self.field_counts.get_remaining_goals() > 1
            ):
                return [goal] + self.__generate_goal_list(
                    pose, percentage, discount, current_iter + 1
                )
            else:
                return [goal]
        return []

    def __generate_robot_list(
        self,
        random_color: int,
        pose: Pose2D,
        percentage: float,
        discount: float,
        current_iter: int = 0,
    ) -> list[Robot]:
        robot_num = random.randint(0, 2)

        robot = None
        if robot_num == 0 and self.field_counts.get_remaining_host_robots() > 0:
            robot = HostRobot(self.__get_alliance_color(random_color), pose)
            self.field_counts.host_robots += 1
        elif robot_num == 1 and self.field_counts.get_remaining_partner_robots() > 0:
            robot = PartnerRobot(self.__get_alliance_color(random_color), pose)
            self.field_counts.partner_robots += 1
        elif robot_num == 2 and self.field_counts.get_remaining_opposing_robots() > 0:
            robot = OpposingRobot(self.__get_alliance_color(random_color, False), pose)
            self.field_counts.partner_robots += 1
        else:
            getLogger(REPRESENTATION_LOGGER_NAME).error(
                f"Attempting to spawn robot of number {robot_num} when all robots are spawned"
            )

        if robot is not None:
            getLogger(REPRESENTATION_LOGGER_NAME).info(
                f"Spawned {type(robot).__name__} of color {robot.color} at ({robot.pose.x},{robot.pose.y})"
            )

            if random.random() < SPAWN_GOAL_IN_ROBOT:
                robot.goals = robot.goals + self.__generate_goal_list(
                    pose, SPAWN_GOAL_IN_ROBOT, ADDITIONAL_GOAL_IN_ROBOT_DISCOUNT_FACTOR
                )

            if random.random() < SPAWN_RING_IN_ROBOT:
                robot.rings = robot.rings + self.__generate_ring_list(
                    pose, SPAWN_RING_IN_ROBOT, ADDITIONAL_RING_IN_ROBOT_DISCOUNT_FACTOR
                )

            if (
                percentage < (percentage * ((current_iter + 1) * discount))
                and self.field_counts.get_remaining_robots() > 1
            ):
                return [robot] + self.__generate_robot_list(
                    random_color, pose, percentage, discount, current_iter + 1
                )
            else:
                return [robot]
        return []

    def randomize(self) -> None:
        # Reset field
        self.red_platform.state = PlatformState.LEVEL
        self.red_platform.robots = []
        self.red_platform.goals = []
        self.red_platform.rings = []

        self.blue_platform.state = PlatformState.LEVEL
        self.blue_platform.robots = []
        self.blue_platform.goals = []
        self.blue_platform.rings = []

        self.robots = []
        self.goals = []
        self.rings = []

        self.field_counts = FieldCounts()

        # Randomize field
        field_map = np.zeros((FIELD_WIDTH_IN + 1, FIELD_WIDTH_IN + 1))

        # Prevent things from spawning in on the ramp
        mid_field = int(FIELD_WIDTH_IN / 2)
        for x in range(
            mid_field - int(PLATFORM_LENGTH_IN / 2),
            mid_field + int(PLATFORM_LENGTH_IN / 2),
        ):
            for y in range(0, PLATFORM_WIDTH_IN + 1):
                field_map[y][x] = 1  # Block off area for ramp

            for y in range(FIELD_WIDTH_IN - PLATFORM_WIDTH_IN, FIELD_WIDTH_IN + 1):
                field_map[y][x] = 1  # Block off area for ramp

        current_color = random.randint(0, 1)

        # TODO fix when entities are stacked

        for ramp_color in [Color.RED, Color.BLUE]:
            x_pos = (0 - (PLATFORM_LENGTH_IN / 2)) + 5
            y_pos = (
                (PLATFORM_WIDTH_IN / 3)
                if ramp_color == Color.RED
                else (144 - (PLATFORM_WIDTH_IN / 3))
            )

            # TODO add logging to ramp generated elements

            robots = []
            if random.random() < SPAWN_ROBOT_ON_RAMP:
                pose = Pose2D(x_pos, y_pos)
                x_pos += 10
                robots = self.__generate_robot_list(
                    current_color,
                    pose,
                    SPAWN_ROBOT_ON_RAMP,
                    ADDITIONAL_ROBOT_ON_RAMP_DISCOUNT_FACTOR,
                )

            goals = []
            if random.random() < SPAWN_GOAL_ON_RAMP:
                pose = Pose2D(x_pos, y_pos)
                x_pos += 10
                goals = self.__generate_goal_list(
                    pose, SPAWN_GOAL_ON_RAMP, ADDITIONAL_GOAL_ON_RAMP_DISCOUNT_FACTOR
                )

            rings = []
            if random.random() < SPAWN_RING_ON_RAMP:
                pose = Pose2D(x_pos, y_pos)
                x_pos += 10
                rings = self.__generate_ring_list(
                    pose, SPAWN_RING_ON_RAMP, ADDITIONAL_RING_ON_RAMP_DISCOUNT_FACTOR
                )

            statePercent = random.random()
            if statePercent < 0.33:
                state = PlatformState.LEFT
            elif statePercent <= 0.66:
                state = PlatformState.LEVEL
            else:
                state = PlatformState.RIGHT

            if ramp_color == Color.RED:
                self.red_platform = RedPlatform(
                    state, robots=robots, goals=goals, rings=rings
                )
            else:
                self.blue_platform = BluePlatform(
                    state, robots=robots, goals=goals, rings=rings
                )

        while self.field_counts.get_remaining_host_robots() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                robot = HostRobot(
                    self.__get_alliance_color(current_color), Pose2D(x, y)
                )

                if random.random() < SPAWN_GOAL_IN_ROBOT:
                    robot.goals = robot.goals + self.__generate_goal_list(
                        pose,
                        SPAWN_GOAL_IN_ROBOT,
                        ADDITIONAL_GOAL_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                if random.random() < SPAWN_RING_IN_ROBOT:
                    robot.rings = robot.rings + self.__generate_ring_list(
                        pose,
                        SPAWN_RING_IN_ROBOT,
                        ADDITIONAL_RING_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                self.robots.append(robot)
                self.field_counts.host_robots += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Host Robot at ({x},{y})"
                )

        while self.field_counts.get_remaining_partner_robots() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                robot = PartnerRobot(self.__get_alliance_color(current_color), pose)

                if random.random() < SPAWN_GOAL_IN_ROBOT:
                    robot.goals = robot.goals + self.__generate_goal_list(
                        pose,
                        SPAWN_GOAL_IN_ROBOT,
                        ADDITIONAL_GOAL_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                if random.random() < SPAWN_RING_IN_ROBOT:
                    robot.rings = robot.rings + self.__generate_ring_list(
                        pose,
                        SPAWN_RING_IN_ROBOT,
                        ADDITIONAL_RING_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                self.robots.append(robot)
                self.field_counts.partner_robots += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Partner Robot at ({x},{y})"
                )

        while self.field_counts.get_remaining_opposing_robots() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                robot = OpposingRobot(
                    self.__get_alliance_color(current_color, False), pose
                )

                if random.random() < SPAWN_GOAL_IN_ROBOT:
                    robot.goals = robot.goals + self.__generate_goal_list(
                        pose,
                        SPAWN_GOAL_IN_ROBOT,
                        ADDITIONAL_GOAL_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                if random.random() < SPAWN_RING_IN_ROBOT:
                    robot.rings = robot.rings + self.__generate_ring_list(
                        pose,
                        SPAWN_RING_IN_ROBOT,
                        ADDITIONAL_RING_IN_ROBOT_DISCOUNT_FACTOR,
                    )

                self.robots.append(robot)
                self.field_counts.opposing_robots += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Opposing Robot at ({x},{y})"
                )

        while self.field_counts.get_remaining_red_goals() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                goal = RedGoal(pose)

                if random.random() < SPAWN_RING_ON_GOAL:
                    self.__add_rings_to_goal(goal)

                self.goals.append(goal)
                self.field_counts.red_goals += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Red Goal at ({x},{y})"
                )

        while self.field_counts.get_remaining_blue_goals() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                goal = BlueGoal(pose)

                if random.random() < SPAWN_RING_ON_GOAL:
                    self.__add_rings_to_goal(goal)

                self.goals.append(goal)
                self.field_counts.blue_goals += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Blue Goal at ({x},{y})"
                )

        while self.field_counts.get_remaining_low_neutral_goals() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                goal = LowNeutralGoal(pose)

                if random.random() < SPAWN_RING_ON_GOAL:
                    self.__add_rings_to_goal(goal)

                self.goals.append(goal)
                self.field_counts.low_neutral_goals += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned Low Neutral Goal at ({x},{y})"
                )

        while self.field_counts.get_remaining_high_neutral_goals() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                goal = HighNeutralGoal(pose)

                if random.random() < SPAWN_RING_ON_GOAL:
                    self.__add_rings_to_goal(goal)

                self.goals.append(goal)
                self.field_counts.high_neutral_goals += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(
                    f"Spawned High Neutral Goal at ({x},{y})"
                )

        while self.field_counts.get_remaining_rings() > 0:
            grid_x = random.randint(0, FIELD_WIDTH_IN)
            x = grid_x - int(FIELD_WIDTH_IN / 2)
            y = random.randint(0, FIELD_WIDTH_IN)
            pose = Pose2D(x, y)

            if field_map[y][grid_x] == 0:
                field_map[y][grid_x] = 1

                self.rings.append(Ring(pose))
                self.field_counts.rings += 1

                getLogger(REPRESENTATION_LOGGER_NAME).info(f"Spawned Ring at ({x},{y})")

    def draw(self) -> plt.plot:
        combined_ring_arr = (
            self.rings + self.red_platform.rings + self.blue_platform.rings
        )
        combined_goal_arr = (
            self.goals + self.red_platform.goals + self.blue_platform.goals
        )
        combined_robot_arr = (
            self.robots + self.red_platform.robots + self.blue_platform.robots
        )

        # TODO determine how to draw rings and goals that are posessed by a robot

        # Calculate ring positions
        ring_arr = np.array([[ring.pose.x, ring.pose.y] for ring in combined_ring_arr])

        # Calculate goal positions
        red_goal_arr = np.array(
            [
                [goal.pose.x, goal.pose.y]
                for goal in combined_goal_arr
                if isinstance(goal, RedGoal)
            ]
        )

        blue_goal_arr = np.array(
            [
                [goal.pose.x, goal.pose.y]
                for goal in combined_goal_arr
                if isinstance(goal, BlueGoal)
            ]
        )

        low_neutral_goal_arr = np.array(
            [
                [goal.pose.x, goal.pose.y]
                for goal in combined_goal_arr
                if isinstance(goal, LowNeutralGoal)
            ]
        )

        high_neutral_goal_arr = np.array(
            [
                [goal.pose.x, goal.pose.y]
                for goal in combined_goal_arr
                if isinstance(goal, HighNeutralGoal)
            ]
        )

        # Calculate robot positions
        host_robot_arr = np.array(
            [
                [robot.pose.x, robot.pose.y, convertColorToRGBA(robot.color)]
                for robot in combined_robot_arr
                if isinstance(robot, HostRobot)
            ],
            dtype=object,
        )

        partner_robot_arr = np.array(
            [
                [robot.pose.x, robot.pose.y, convertColorToRGBA(robot.color)]
                for robot in combined_robot_arr
                if isinstance(robot, PartnerRobot)
            ],
            dtype=object,
        )

        opposing_robot_arr = np.array(
            [
                [robot.pose.x, robot.pose.y, convertColorToRGBA(robot.color)]
                for robot in combined_robot_arr
                if isinstance(robot, OpposingRobot)
            ],
            dtype=object,
        )

        # Draw elements
        fig, ax = plt.subplots(figsize=FIG_SIZE)

        # Draw platforms
        red_plat = mpatches.Rectangle(
            (0 - (PLATFORM_LENGTH_IN / 2), 0),
            PLATFORM_LENGTH_IN,
            PLATFORM_WIDTH_IN,
            fill=True,
            fc=(1, 0, 0, 0.2),
            ec=(1, 0, 0, 0),
            linewidth=2,
        )

        blue_plat = mpatches.Rectangle(
            (
                0 - (PLATFORM_LENGTH_IN / 2),
                (FIELD_WIDTH_IN - PLATFORM_WIDTH_IN),
            ),  # x, y of bottom left corner
            PLATFORM_LENGTH_IN,
            PLATFORM_WIDTH_IN,
            fill=True,
            fc=(0, 0, 1, 0.2),
            ec=(0, 0, 1, 0),
            linewidth=2,
        )

        ax.add_patch(red_plat)
        ax.add_patch(blue_plat)

        # Draw robots
        if np.any(host_robot_arr):
            ax.scatter(
                host_robot_arr[:, 0],
                host_robot_arr[:, 1],
                color=host_robot_arr[:, 2],
                ec="black",
                linewidth=4,
                marker="s",
                s=3000,
            )

        if np.any(partner_robot_arr):
            ax.scatter(
                partner_robot_arr[:, 0],
                partner_robot_arr[:, 1],
                color=partner_robot_arr[:, 2],
                marker="s",
                s=3000,
            )

        if np.any(opposing_robot_arr):
            ax.scatter(
                opposing_robot_arr[:, 0],
                opposing_robot_arr[:, 1],
                color=opposing_robot_arr[:, 2],
                marker="s",
                s=3000,
            )

        # Draw goals
        if np.any(red_goal_arr):
            ax.scatter(
                red_goal_arr[:, 0], red_goal_arr[:, 1], color="red", marker="H", s=2000
            )

        if np.any(blue_goal_arr):
            ax.scatter(
                blue_goal_arr[:, 0],
                blue_goal_arr[:, 1],
                color="blue",
                marker="H",
                s=2000,
            )

        if np.any(low_neutral_goal_arr):
            ax.scatter(
                low_neutral_goal_arr[:, 0],
                low_neutral_goal_arr[:, 1],
                color="yellow",
                marker="H",
                s=2000,
            )

        if np.any(high_neutral_goal_arr):
            ax.scatter(
                high_neutral_goal_arr[:, 0],
                high_neutral_goal_arr[:, 1],
                color="yellow",
                marker="H",
                s=2000,
            )

        # Draw rings
        if np.any(ring_arr):
            ax.scatter(ring_arr[:, 0], ring_arr[:, 1], color="purple")

        ax.set_xlim([-72, 72])
        ax.set_ylim([0, 144])

        return ax

    def export_to_dict(self) -> dict:
        loc = np.zeros((145, 145, 100))
        pos = np.zeros((100, 3, 2))
        col = np.zeros((100))
        val = np.zeros((100))
        opp = np.zeros((100))

        # TODO: add platforms
        ent_lst = [*self.rings, *self.goals, *self.robots]
        pose_lam = lambda en: (
            max(min(round(en.pose.x), 144), 0),
            max(min(round(en.pose.y), 144), 0),
        )

        def type_map(ent):
            val = 2
            if isinstance(ent, HighNeutralGoal):
                val = 0
            elif isinstance(ent, Goal):
                val = 1
            elif isinstance(ent, Ring):
                val = 2
            elif isinstance(ent, Robot):
                val = 3
            return val

        def point_map(ent):
            val = 0
            # TODO: compress util funcs into field rep class
            host_col = [robot for robot in self.robots if type(robot) is HostRobot][
                0
            ].color
            if isinstance(ent, HighNeutralGoal):
                val = 0
            elif isinstance(ent, Goal):
                val = ent.get_current_score(host_col)
            elif isinstance(ent, Ring):
                val = 1
            elif isinstance(ent, Robot):
                val = sum([goal.get_current_score(host_col) for goal in ent.goals])
                val += len(ent.rings)
            return val

        for i, ent in enumerate(ent_lst):
            # id = i
            # location
            x, y = pose_lam(ent)
            loc[x][y][i] = type_map(ent)

            # possesion and opposing
            if isinstance(ent, Goal):
                for level, cont in ent.ring_containers.items():
                    ldx = 0
                    if level == GoalLevel.BASE:
                        ldx = 0
                    elif level == GoalLevel.LOW:
                        ldx = 1
                    elif level == GoalLevel.HIGH:
                        ldx = 2
                    pos[i][ldx][0] = cont.get_utilization()
            if isinstance(ent, Robot):
                pos[i][0][1] = len(ent.rings)
                pos[i][0][0] = len(ent.goals)

                opp[i] = ent.id

            # color
            if not isinstance(ent, Ring):
                col[i] = ent.color.value

            # value
            val[i] = point_map(ent)

        return dict(location=loc, possesion=pos, color=col, value=val, is_opposing=opp)

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: FieldRepresentation, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation

    def __calculate_potential_score(self) -> None:
        return None  # TODO

    def get_current_representation(self) -> FieldRepresentation:
        return self.field_representation

    def get_current_time(self) -> int:
        return self.current_time

    def get_potential_score(self) -> Tuple[int, int]:
        return self.potential_score

    def get_current_score(self) -> Tuple[int, int]:
        return self.potential_score if self.current_time <= 0 else (0, 0)
