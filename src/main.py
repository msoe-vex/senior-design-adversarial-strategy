from examples.fieldRepresentation.field_representations import basic_goal_representation

if __name__ == "__main__":
    fieldRep = basic_goal_representation()
    print(fieldRep.as_json())
