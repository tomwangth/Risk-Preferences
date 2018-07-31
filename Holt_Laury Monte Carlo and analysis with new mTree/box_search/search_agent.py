from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message_space import Message
from random import *


@directive_enabled_class
class SearchAgent(Agent):
    def __init__(self):
        print("a class has been created... or something")
        self.property_x = 1
        self.property_y = 2
        self.box_list = None
        self.institution = None

    @directive_decorator("initialize_agent")
    def initialize_agent(self, message:Message):
        print("initializing agent")
        payload = message.get_payload()
        self.institution = payload["institution"]

    @directive_decorator("start_agent")
    def start_agent(self, message):
        print("starting the agent...")

    @directive_decorator("setup_boxes")
    def setup_boxes(self, message:Message):
        payload = message.get_payload()
        self.box_list = payload["box_list"]

    @directive_decorator("make_choice")
    def make_choice(self, message):
        print("received choices from institution...")
        element_selected = self.select_box()
        choice_message = Message()
        choice_message.set_sender(self)
        choice_message.set_directive("choice")
        choice_message.set_payload({"selected_element": element_selected})
        self.send(self.institution, choice_message)

    def select_box(self):
        random_element = randrange(0, len(self.box_list))
        box_value = self.box_list[random_element]
        if box_value == "R":
            random_element = self.select_box()
        return random_element

