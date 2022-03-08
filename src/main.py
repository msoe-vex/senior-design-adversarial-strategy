import matplotlib.pyplot as plt
from entities.fieldConfigurations import (
    basic_goal_representation,
    basic_ring_representation,
    ending_representation,
    starting_representation,
)

if __name__ == "__main__":
    fieldRep = starting_representation()
    print(fieldRep.as_json())
    # fig = fieldRep.draw()
    # plt.show()

    # plat = RedPlatform(PlatformState.LEVEL)
    # print(plat)
