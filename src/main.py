from tracemalloc import start
import matplotlib.pyplot as plt
from entities.fieldConfigurations import (
    basic_goal_representation,
    basic_ring_representation,
    ending_representation,
    starting_representation,
)
from loggingManager import configure_loggers

if __name__ == "__main__":
    configure_loggers()
    
    fieldRep = starting_representation()
    fieldRep.randomize()

    fig = fieldRep.draw()
    plt.show()
