from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message_space import Message




@directive_enabled_class
class BasicAgent(Agent):
    def __init__(self):
        print("an agent has been ")
        self.property_x = 1
        self.property_y = 2

    @directive_decorator("start_agent")
    def start_agent(self, message:Message):
        print("starting the agent...")
        self.experiment_log("test")