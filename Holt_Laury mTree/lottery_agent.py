from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message_space import Message
import numpy as np
import math as mat

@directive_enabled_class
class BasicAgent(Agent):
    def __init__(self):
        self.agent_id = None
        self.choice = []
        self.institutions =[] # make sure to populate this
        self.payoff = []


    @directive_decorator("initialize_agents")
    def initialize_agents(self, message:Message):
        '''give the agent its theta and delta'''

        payload = message.get_payload()
        self.agent_id = payload["agent_id"]

    @directive_decorator("fill_in_institution")
    def fill_in_institution(self, message: Message):
        ''' let the agent know the institution '''

        payload = message.get_payload()
        self.institutions = payload["institutions"]


    @directive_decorator("make_choice")
    def make_choice(self, message:Message):  # get row from bundle
        '''agent makes their choice'''
        payload = message.get_payload()
        row = payload["row"]
        OptionA = row[0]
        OptionB = row[1]
        choice = input("You choose:")
        if choice == "A":
            self.choice.append(OptionA)
        elif choice == "B":
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


    @directive_decorator("get payoff")
    def get_payoff(self, message: Message):
        '''agent receive payoff after completion of all lotteries'''

        payload = message.get_payload()
        self.payoff.append(payload["payoff"])
        print("You received:", payload["payoff"])
