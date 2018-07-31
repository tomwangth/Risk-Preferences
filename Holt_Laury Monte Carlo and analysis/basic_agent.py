from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message_space import Message
import numpy as np



@directive_enabled_class
class BasicAgent(Agent):
    def __init__(self):
        #print("An agent has been created.")
        self.theta = None # for making sure it is changed
        self.delta = None # for making sure it is changed
        self.epsilon = None
        self.choice = []
        self.institutions =[] # make sure to populate this


    @directive_decorator("initialize_agents")
    def initialize_agents(self, message:Message):
        '''give the agenst their theta and sd'''

        payload = message.get_payload()
        self.theta = payload["theta"]
        self.delta = payload["delta"]
        self.epsilon = payload["epsilon"]


    @directive_decorator("fill_in_institution")
    def fill_in_institution(self, message: Message):
        ''' gives the agent a list of institutions '''
        payload = message.get_payload()
        self.institutions = payload["institutions"]

    def CRRA(self,value,theta):
        ''' helper function to calculate crra'''
        if theta == 1.0:
            if value == 0.0:  # Handle value = 0.0
                return 0.0
            else:
                return mat.log(value)
        else:
            if value == 0.0:  # Handle value = 0.0
                return 0.0
            else:
                return (1.0 / (1.0 - theta)) * (value) ** (1.0 - theta)


#TODO put epsilon in the make_choice

    @directive_decorator("make_choice")
    def make_choice(self, message:Message):  # get row from bundle
        '''agent makes their choice here'''

        #the agents gets the row and sd
        payload = message.get_payload()
        row = payload["row"]
        delta = self.delta

        #calculates the theta w/ normal distributed sd
        if delta ==0:
            error = 0
        else:
            error = np.random.triangular(-delta, 0, delta)

        theta = self.theta + error + self.epsilon

        OptionA = row[0] # tuple of option 1
        OptionB = row[1] # tuple of optoin 2

        if len(OptionA) != len(OptionB):  # ensure that there is no error in the row data
            raise ValueError("Length of options must be the same")

        # the probability and utility of OptionA Choice 1
        prob_a1 = (OptionA[0][0])
        out_a1 = self.CRRA(OptionA[0][1], theta)


        # the probability and utility OptionA Choice 2
        prob_a2 = OptionA[1][0]
        out_a2 = self.CRRA(OptionA[1][1], theta)

        # the probability and utility OptionB Choice 1
        prob_b1 = (OptionB[0][0])
        out_b1 = self.CRRA(OptionB[0][1], theta)

        # the probability and utility OptionB Choice 2
        prob_b2 = OptionB[1][0]
        out_b2 = self.CRRA(OptionB[1][1], theta)

        # expected utility of OptionA and OptionB
        util_a = prob_a1 * out_a1 + prob_a2 * out_a2
        util_b = prob_b1 * out_b1 + prob_b2 * out_b2

        # selects and records the option with larger expected utility
        if util_a > util_b:
            self.choice.append(OptionA)

        else:
            self.choice.append(OptionB)

    @directive_decorator("grab_response")
    def grab_response(self, message:Message):
        '''send the response back to the institution'''


        #create message
        message = Message()
        message.set_sender(self)
        message.set_directive("returned_response")

        #make payload
        payload = {}
        payload["choice"] = self.choice
        #print(self.choice)
        message.set_payload(payload)
        #for i in self.institutions:
        self.send(self.institutions[0],message)
        self.choice = []
