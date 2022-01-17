from entities.platforms import BluePlatform, PlatformState
from examples.fieldRepresentation.field_representations import basic_goal_representation, basic_ring_representation, ending_representation, starting_representation

if __name__ == "__main__":
    fieldRep = ending_representation()
    print(fieldRep.as_json())
