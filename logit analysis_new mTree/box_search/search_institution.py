from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.directive_decorators import *
from random import *


@directive_enabled_class
class SearchInstitution(Institution):
    def __init__(self):
        print("institution started")
        self.agents = None
        self.box_list = None
        self.redacted_box_list = None


    @directive_decorator("choice")
    def agent_choice(self, message):
        print("received agent choice...")

    @directive_decorator("initialize_institution")
    def initialize_institution(self, message:Message):
        print("initializing an institution")
        payload = message.get_payload()
        self.agents = payload["agent_list"]


    @directive_decorator("prepare_box_list")
    def prepare_box_list(self, message):
        print("Received list of boxes from environment")
        payload = message.get_payload()
        self.box_list = payload["box_list"]
        print("Institution box list configured: " + str(self.box_list))
        self.agents = payload["agent_list"]
        print("Agents configured: " + str(self.agents))

    @directive_decorator("start_round")
    def start_round(self, message:Message):
        print("Getting a start round request from the environment")
        # first we will redact the box list for use with the agents.
        self.redact_box_list()
        # now we can send a redacted box list to the agent and then we can tell them to make a choice
        setup_agent_box_list_message = Message()
        setup_agent_box_list_message.set_sender(self)
        setup_agent_box_list_message.set_directive("setup_boxes")
        setup_agent_box_list_message.set_payload({"box_list": self.redacted_box_list})
        for agent in self.agents:
            self.send(agent, setup_agent_box_list_message)

        # now we can send a redacted box list to the agent and then we can tell them to make a choice
        agent_choice_message = Message()
        agent_choice_message.set_sender(self)
        agent_choice_message.set_directive("make_choice")
        for agent in self.agents:
            self.send(agent, agent_choice_message)

    def redact_box_list(self):
        self.redacted_box_list = list(self.box_list)
        random_element = randrange(0, len(self.redacted_box_list))
        self.redacted_box_list[random_element] = "R"
