from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.directive_decorators import *



@directive_enabled_class
class BasicInstitution(Institution):
    def __init__(self):
        print("institution started")
        self.agents = []
        self.experiment_log("institution started")


