from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *


@directive_enabled_class
class BasicEnvironment(Environment):
    def __init__(self):
        self.institutions = []
        self.agents = []

        self.boxes = []

    @directive_decorator("initialize_boxes")
    def initialize_boxes(self, message:Message):
        print("Received Message")
        print(self.boxes)
        self.boxes.append(1)
        print(self.boxes)
        print("self stuff")
        print(str(self))
        print(self.agents)

    @directive_decorator("start_agents")
    def start_agents(self, message: Message):
        print("About to start agents")
        for agent in self.agents:
            message = Message()
            message.set_sender(self)
            message.set_directive("start_agent")
            self.send(agent, message)
