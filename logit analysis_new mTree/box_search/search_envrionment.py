from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *


@directive_enabled_class
class SearchEnvironment(Environment):
    def __init__(self):
        self.institutions = []
        self.agents = []

        self.box_list = None

        self.goods = []
        print("environment started...")
        self.out_link = None

        #self.createActor(BasicAgent)
        #self.create_institution(BasicInstitution)
        #self.create_agents(BasicAgent, 1)

    @directive_decorator("initialize_boxes")
    def initialize_boxes(self, message:Message):
        print("Initializing boxes inside environment")
        payload = message.get_payload()
        box_list = payload["box_list"]
        self.box_list = box_list
        print(self.box_list)
        print("Now sending box list to the institution for use")
        message = Message()
        message.set_directive("prepare_box_list")

        payload = {}
        payload["box_list"] = self.box_list
        # we will also send the agent list to the institution for it to keep track of
        payload["agent_list"] = self.agents
        message.set_payload(payload)
        self.send(self.institutions[0], message)

    @directive_decorator("initialize_round")
    def initialize_round(self, message: Message):
        print("About to initialize an experiment round by sending a messsage to the institution")
        # initialize institution by alerting to agents
        message = Message()
        message.set_directive("initialize_institution")
        message.set_payload({"agent_list": self.agents})
        self.send(self.institutions[0], message)
        # initialize agents by alerting to institution
        message = Message()
        message.set_directive("initialize_agent")
        message.set_payload({"institution": self.institutions[0]})
        for agent in self.agents:
            self.send(agent, message)

    @directive_decorator("start_agents")
    def start_agents(self, message: Message):
        print("About to start agents")
        for agent in self.agents:
            message = Message()
            message.set_sender(self)
            #message.set_recipient(agent)
            message.set_directive("start_agent")
            self.send(agent, message)

    @directive_decorator("start_round")
    def start_round(self, message: Message):
        print("Start round message received... forwarding to institution")
        message = Message()
        message.set_sender(self)
        message.set_recipients(self.institutions[0])
        message.set_directive("start_round")
        self.send(self.institutions[0], message)