import matplotlib.pyplot as plt
from entities.mathUtils import Pose2D
from entities.platforms import BluePlatform, PlatformState, RedPlatform
from entities.scoring_elements import Ring
from entities.fieldConfigurations import basic_goal_representation, basic_ring_representation, ending_representation, starting_representation

if __name__ == "__main__":
    fieldRep = ending_representation()
    print(fieldRep)
    # fig = fieldRep.draw()
    # plt.show()

    # plat = RedPlatform(PlatformState.LEVEL)
    # print(plat)

