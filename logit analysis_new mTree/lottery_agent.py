from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message_space import Message
import numpy as np
import math as mat

@directive_enabled_class
class BasicAgent(Agent):
    def __init__(self):
        self.theta = None # for making sure it is changed every run
        self.delta = None # for making sure it is changed every run
        self.epsilon = None # for making sure it is changed every run
        self.error = None #realized delta
        self.e = None  # for realized epsilon
        self.choice = []
        self.institutions =[] # make sure to populate this
        self.payoff = []


    @directive_decorator("initialize_agents")
    def initialize_agents(self, message:Message):
        '''give the agent its theta and delta'''

        payload = message.get_payload()
        self.theta = payload["theta"]
        self.delta = payload["delta"]
        self.epsilon = payload["epsilon"]

    @directive_decorator("fill_in_institution")
    def fill_in_institution(self, message: Message):
        ''' let the agent know the institution '''

        payload = message.get_payload()
        self.institutions = payload["institutions"]

    def CRRA(self,value,theta):
        ''' CRRA calculation'''

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

    @directive_decorator("make_choice")
    def make_choice(self, message:Message):  # get row from bundle
        '''agent makes their choice'''

        #the agents gets the row and sd
        payload = message.get_payload()
        row = payload["row"]

        delta = self.delta

        #calculates the theta w/ triangularlly distributed delta
        if delta ==0:
            self.error = 0
        else:
            self.error = np.random.triangular(-delta, 0, delta)

        theta = self.theta + self.error

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

        e = self.epsilon

        # calculates the utility w/ triangularlly distributed epsilon
        if e == 0:
            self.e = 0
        else:
            self.e = np.random.triangular(-e, 0, e)

        # expected utility of OptionA and OptionB
        util_a = prob_a1 * out_a1 + prob_a2 * out_a2 + self.e
        util_b = prob_b1 * out_b1 + prob_b2 * out_b2 + self.e

        # selects and records the option with larger expected utility
        if util_a > util_b:
            self.choice.append(OptionA)

        else:
            self.choice.append(OptionB)



    @directive_decorator("get_response")
    def grab_response(self, message:Message):
        '''send the response back to the institution'''

        #create message
        message = Message()
        message.set_sender(self)
        message.set_directive("returned_response")

        #make payload
        payload = {}
        payload["choice"] = self.choice
        message.set_payload(payload)
        self.send(self.institutions[0],message)
        self.choice = []
        self.error = None

    @directive_decorator("get payoff")
    def get_payoff(self, message: Message):
        '''agent receive payoff after completion of all lotteries'''

        payload = message.get_payload()
        self.payoff.append(payload["payoff"])
        print("Agent received:", payload["payoff"])
