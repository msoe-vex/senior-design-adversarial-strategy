from __future__ import annotations
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Tuple
from dataclasses import dataclass, field
from entities.constants import *
from entities.enumerations import Color, convertColorToRGBA
from entities.interfaces import ISerializable
from entities.math_utils import Pose2D
from entities.platforms import Platform, PlatformState, RedPlatform, BluePlatform
from entities.scoring_elements import BlueGoal, GoalLevel, Goal, NeutralGoal, RedGoal, Ring, RingContainer
from entities.robots import HostRobot, OpposingRobot, PartnerRobot, Robot, RobotID


@dataclass
class Field(ISerializable):
    red_platform: RedPlatform = RedPlatform(PlatformState.LEVEL)
    blue_platform: BluePlatform = BluePlatform(PlatformState.LEVEL)
    rings: List[Ring] = field(default_factory=list)
    goals: List[Goal] = field(default_factory=list)
    robots: List[Robot] = field(default_factory=list)

    def __parse_position(self, position_dict: dict) -> Pose2D:
        x = position_dict["x"]
        y = position_dict["y"]
        return Pose2D(x, y)

    def __parse_rings(self, ring_dict: dict) -> List[Ring]:
        rings = []
        for ring in ring_dict:
            pose = self.__parse_position(ring["position"])
            rings.append(Ring(pose))

        return rings

    def __parse_ring_container(self, ring_container_dict: dict) -> RingContainer:
        max_storage = ring_container_dict["max_storage"]

        rings = self.__parse_rings(ring_container_dict["rings"])

        return RingContainer(max_storage, rings)

    def __parse_ring_containers(self, ring_containers_dict: dict) -> dict[GoalLevel, RingContainer]:
        ring_containers = {}

        base_ring_container = ring_containers_dict.get("BASE")

        if base_ring_container:
            ring_containers[GoalLevel.BASE] = self.__parse_ring_container(base_ring_container)

        low_ring_container =ring_containers_dict.get("LOW")

        if low_ring_container:
            ring_containers[GoalLevel.LOW] = self.__parse_ring_container(low_ring_container)

        high_ring_container = ring_containers_dict.get("HIGH")

        if high_ring_container:
            ring_containers[GoalLevel.HIGH] = self.__parse_ring_container(high_ring_container)

        return ring_containers

    def __parse_goals(self, goal_dict: dict) -> List[Goal]:
        goals = []
        for goal in goal_dict:
            color = goal["color"]         

            pose = self.__parse_position(goal["position"])

            ring_containers = self.__parse_ring_containers(goal["ring_containers"])

            tipped = goal["tipped"]

            if color == Color.RED:
                goals.append(RedGoal(pose, ring_containers=ring_containers, tipped=tipped))
            elif color == Color.BLUE:
                goals.append(BlueGoal(pose, ring_containers=ring_containers, tipped=tipped))
            else:
                goals.append(NeutralGoal(pose, ring_containers=ring_containers, tipped=tipped))

        return goals

    def __parse_robots(self, robots_dict: dict) -> Robot:
        robots = []
        for robot in robots_dict:
            color = robot["color"]

            id = robot["id"]

            pose = self.__parse_position(robot["position"])

            rings = self.__parse_ring_containers(robot["rings"])

            goals = self.__parse_goals(robot["goals"])

            tipped = robot["tipped"]

            if id == RobotID.SELF:
                robots.append(HostRobot(color, pose, rings=rings, goals=goals, tipped=tipped))
            elif id == RobotID.PARTNER:
                robots.append(PartnerRobot(color, pose, rings=rings, goals=goals, tipped=tipped))
            else:
                robots.append(OpposingRobot(color, pose, rings=rings, goals=goals, tipped=tipped))

        return robots

    def __parse_platform(self, platform_dict: dict) -> Platform:
        color = platform_dict["color"]

        goals = self.__parse_goals(platform_dict["goals"])

        rings = self.__parse_rings(platform_dict["rings"])

        robots = self.__parse_robots(platform_dict["robots"])

        state = platform_dict["state"]

        if color == Color.RED:
            return RedPlatform(state, rings=rings, goals=goals, robots=robots)
        else:
            return BluePlatform(state, rings=rings, goals=goals, robots=robots)

    def parse_representation(self, representation: str) -> None:
        self.rings = self.__parse_rings(representation["rings"])

        self.goals = self.__parse_goals(representation["goals"])

        self.red_platform = self.__parse_platform(representation["red_platform"])
        
        self.blue_platform = self.__parse_platform(representation["blue_platform"])

        self.robots = self.__parse_robots(representation["robots"])

    def randomize(self) -> None:
        fieldMap = np.zeros((FIELD_WIDTH_IN + 1, FIELD_WIDTH_IN + 1))

        # Prevent things from spawning in on the ramp
        for x in range(70 - (PLATFORM_LENGTH_IN / 2), 70 + (PLATFORM_LENGTH_IN / 2)):
            for y in range(0, PLATFORM_WIDTH_IN):
                fieldMap[y][x] = 1 # Block off area for ramp

            for y in range(FIELD_WIDTH_IN - PLATFORM_WIDTH_IN, FIELD_WIDTH_IN):
                fieldMap[y][x] = 1 # Block off area for ramp

        for i in range(MAX_NUM_RINGS):
            pass

        for i in range(MAX_NUM_RED_GOALS):
            pass

        for i in range(MAX_NUM_BLUE_GOALS):
            pass

        for i in range(MAX_NUM_LOW_NEUTRAL_GOALS):
            pass

        for i in range(MAX_NUM_HIGH_NEUTRAL_GOALS):
            pass

        for i in range(MAX_NUM_HOST_ROBOTS):
            pass

        for i in range(MAX_NUM_PARTNER_ROBOTS):
            pass

        for i in range(MAX_NUM_OPPOSING_ROBOTS):
            pass

    def draw(self) -> plt.plot:
        combined_ring_arr = self.rings #+ self.red_platform.rings + self.blue_platform.rings
        combined_goal_arr = self.goals #+ self.red_platform.goals + self.blue_platform.goals
        combined_robot_arr = self.robots #+ self.red_platform.robots + self.blue_platform.robots

        # Calculate ring positions
        ring_arr = np.array([[ring.position.x, ring.position.y] for ring in combined_ring_arr])

        # Calculate goal positions
        red_goal_arr = np.array([[goal.position.x, goal.position.y] for goal in combined_goal_arr if isinstance(goal, RedGoal)])

        blue_goal_arr = np.array([[goal.position.x, goal.position.y] for goal in combined_goal_arr if isinstance(goal, BlueGoal)])

        neutral_goal_arr = np.array([[goal.position.x, goal.position.y] for goal in combined_goal_arr if isinstance(goal, NeutralGoal)])

        # Calculate robot positions
        host_robot_arr = np.array([[robot.position.x, robot.position.y, convertColorToRGBA(robot.color)] for robot in combined_robot_arr if isinstance(robot, HostRobot)], dtype=object)

        partner_robot_arr = np.array([[robot.position.x, robot.position.y, convertColorToRGBA(robot.color)] for robot in combined_robot_arr if isinstance(robot, PartnerRobot)], dtype=object)

        opposing_robot_arr = np.array([[robot.position.x, robot.position.y, convertColorToRGBA(robot.color)] for robot in combined_robot_arr if isinstance(robot, OpposingRobot)], dtype=object)

        # Draw elements
        fig, ax = plt.subplots(figsize=FIG_SIZE)

        # Draw rings
        if np.any(ring_arr):
            ax.scatter(ring_arr[:,0], ring_arr[:,1], color="purple")

        # Draw goals
        if np.any(red_goal_arr):
            ax.scatter(red_goal_arr[:,0], red_goal_arr[:,1], color="red", marker="H", s=2000)

        if np.any(blue_goal_arr):
            ax.scatter(blue_goal_arr[:,0], blue_goal_arr[:,1], color="blue", marker="H", s=2000)

        if np.any(neutral_goal_arr):
            ax.scatter(neutral_goal_arr[:,0], neutral_goal_arr[:,1], color="yellow", marker="H", s=2000)

        # Draw robots
        if np.any(host_robot_arr):
            ax.scatter(host_robot_arr[:,0], host_robot_arr[:,1], color=host_robot_arr[:,2], ec="black", linewidth=4, marker="s", s=3000)

        if np.any(partner_robot_arr):
            ax.scatter(partner_robot_arr[:,0], partner_robot_arr[:,1], color=partner_robot_arr[:,2], marker="s", s=3000)

        if np.any(opposing_robot_arr):
            ax.scatter(opposing_robot_arr[:,0], opposing_robot_arr[:,1], color=opposing_robot_arr[:,2], marker="s", s=3000)

        # Draw platforms
        red_plat = mpatches.Rectangle(
            (0 - (PLATFORM_LENGTH_IN / 2), 0),
            PLATFORM_LENGTH_IN,
            PLATFORM_WIDTH_IN,
            fill=True,
            fc=(1, 0, 0, 0.2),
            ec=(1, 0, 0, 0),
            linewidth=2
        )

        blue_plat = mpatches.Rectangle(
            (0 - (PLATFORM_LENGTH_IN / 2), (FIELD_WIDTH_IN - PLATFORM_WIDTH_IN)), # x, y of bottom left corner
            PLATFORM_LENGTH_IN,
            PLATFORM_WIDTH_IN,
            fill=True,
            fc=(0, 0, 1, 0.2),
            ec=(0, 0, 1, 0),
            linewidth=2
        )

        ax.add_patch(red_plat)
        ax.add_patch(blue_plat)

        ax.set_xlim([-72, 72])
        ax.set_ylim([0, 144])

        return ax

    def as_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FieldState(ISerializable):
    def __init__(self, representation: Field, time: int):
        self.potential_score = (0, 0)
        self.current_time = time
        self.field_representation = representation

    def __calculate_potential_score(self) -> None:
        return None  # TODO

    def get_current_representation(self) -> Field:
        return self.field_representation

    def get_current_time(self) -> int:
        return self.current_time

    def get_potential_score(self) -> Tuple[int, int]:
        return self.potential_score

    def get_current_score(self) -> Tuple[int, int]:
        return self.potential_score if self.current_time <= 0 else (0, 0)
