from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *


@directive_enabled_class
class BasicEnvironment(Environment):
    def __init__(self):
        self.institutions = []
        self.agents = []
        self.bundle = []
        self.experiment = None
        self.total_experiments = None
        #self.all_rounds = [] # for each period we store final data here


    @directive_decorator("initialize_rows")
    def initialize_rows(self, message:Message):
        '''makes the rows of the choices as list of tuples'''
        payload = message.get_payload()

        #set the rewards
        reward_A_1 = payload["reward_A_1"]
        reward_A_2 = payload["reward_A_2"]
        reward_B_1 = payload["reward_B_1"]
        reward_B_2 = payload["reward_B_2"]
        num_rows = payload["num_rows"] # number of rows in the bundle

        # creates each row and append to bundle
        for i in range(1, num_rows + 1):
            optionA = ([((i / num_rows), reward_A_1), ((((num_rows - i) / num_rows)), reward_A_2), "A_%d" % i])
            optionB = ([((i / num_rows), reward_B_1), ((((num_rows - i) / num_rows)), reward_B_2), "B_%d" % i])
            self.bundle.append([optionA, optionB]) # append each row to the bundle

        self.experiment = payload["experiment"]
        self.total_experiments = payload["total_experiments"]
        self.run = payload["run"]
        self.total_runs = payload["total_runs"]

    @directive_decorator("send_bundle")
    def send_bundle(self,message:Message):
        ''' sends bundle from environment to institution'''

        #create message to send to institution
        message = Message()
        message.set_sender(self)
        message.set_directive("fill_in_rows")
        payload = {}

        #create the payload w/ bundle
        payload["bundle"] = self.bundle
        payload["experiment"] = self.experiment
        payload["total_experiments"] = self.total_experiments
        payload["run"] = self.run
        payload["total_runs"] = self.total_runs
        message.set_payload(payload)
        self.bundle = []

        #send to all institutions
        for i in self.institutions:
            self.send(i,message)


    @directive_decorator("initialize_agents")
    def initialize_agents(self, message: Message):
        '''give each of the agents their attributes and sends the info to institution for data collecting'''

        # contains the theta and sd
        payload = message.get_payload()
        #self.theta = payload["theta"]
        #self.sd = payload["sd"]

        #make the message to send to each agent
        message = Message()
        message.set_sender(self)
        message.set_directive("initialize_agents")
        message.set_payload(payload)

        #send message to all agents
        for agent in self.agents:
            self.send(agent, message)

        #create message for the institution
        message = Message()
        message.set_sender(self)
        message.set_directive("theta_sd")
        message.set_payload(payload)

        #send the theta and delta to the institution for data collection
        for institution in self.institutions:
            self.send(institution,message)

    @directive_decorator("send_agents")
    def send_agents(self, message: Message):
        '''Send a list of agents to the institutions'''

        #create message to institutions
        message = Message()
        message.set_sender(self)
        message.set_directive("fill_in_agents")

        #create the payload with a list of agents
        payload = {}
        payload["agents"] = self.agents
        message.set_payload(payload)

        #send msg to the institution
        for i in self.institutions:
            self.send(i,message)

    @directive_decorator("send_institution")
    def send_institution(self, message: Message):
        '''Send a list of the institutions to agents '''

        #create message
        message = Message()
        message.set_sender(self)
        message.set_directive("fill_in_institution")

        #create payload with institutions
        payload = {}
        payload["institutions"] = self.institutions
        message.set_payload(payload)

        #send to all agents
        for i in self.agents:
            self.send(i,message)


    @directive_decorator("start_experiment")
    def start_experiment(self, message: Message):
        '''Start the actual experiment'''

        message = Message()
        message.set_sender(self)
        message.set_directive("start_experiment")

        #send the message to all institutions
        for i in self.institutions:
            self.send(i,message)

    @directive_decorator("collect_data")
    def collect_data(self, message: Message):
        '''tells in institution to send the data to the container'''

        #create message
        message = Message()
        message.set_sender(self)
        message.set_directive("collect_data")

        #send to all institutions
        for i in self.institutions:
            self.send(i, message)





