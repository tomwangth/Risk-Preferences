from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.directive_decorators import *
import random
import csv

@directive_enabled_class
class BasicInstitution(Institution):

    def __init__(self):
        self.agents = []
        self.bundles = []
        self.outcome = [] # the outcome of the agent's choice
        self.agent_id = None

        # >>>> data for the experiment <<<<
        self.choice_outcome = [] #actual outcome list, sent to experiment log
        self.outcome_history = []#store all data
        self.payoff_list = [] #store payoffs
        self.risk_preference = None
        self.theta_range = None
        self.est_theta = None



    @directive_decorator("fill_in_bundle")
    def fill_in_rows(self, message: Message):
        ''' puts in the rows into the bundles & set num of experiments/runs '''

        payload = message.get_payload()
        self.bundles = payload["bundle"]




    @directive_decorator("fill_in_agents")
    def fill_in_agents(self, message: Message):
        '''give agents to self'''

        payload = message.get_payload()
        self.agents = payload["agents"]



    @directive_decorator("agent_id")
    def theta_delta(self, message: Message):
        '''keep track of agent's theta, delta'''

        payload = message.get_payload()
        self.agent_id = payload["agent_id"]



    @directive_decorator("start_experiment")
    def start_experiment(self, message: Message):
        '''Starts the experiment for all agents and institutions'''

        #loop through all agents and bundles
        for agent in self.agents:
            print("sending to agent")

            for row in self.bundles:
                #get agent making choice
                payload= {}
                payload["row"] = row
                message = Message()
                message.set_sender(self)
                message.set_directive("make_choice")

                message.set_payload(payload)
                self.send(agent,message)

                #get response from the agent
                message2 = Message()
                message2.set_sender(self)
                message2.set_directive("get_response")
                self.send(self.agents[0],message2)


    def get_theta(self, num_A):

        if num_A == 4:
            self.risk_preference = "risk neutral"
            self.theta_range = (-.15,.15)
            self.est_theta = 0
        elif num_A == 5:
            self.risk_preference = "slightly risk averse"
            self.theta_range = (.15, .41)
            self.est_theta = .28
        elif num_A == 6:
            self.risk_preference = "risk averse"
            self.theta_range = (.41, .68)
            self.est_theta = 0.545
        elif num_A == 7:
            self.risk_preference = "very risk averse"
            self.theta_range = (.68, .97)
            self.est_theta = 0.825
        elif num_A == 8:
            self.risk_preference = "extremely risk averse"
            self.theta_range = (.97, 1.36)
            self.est_theta = 1.165
        elif num_A == 2:
            self.risk_preference = "risk loving"
            self.theta_range = (-.49, -.15)
            self.est_theta = -.32
        elif num_A == 3:
            self.risk_preference = "slightly risk loving"
            self.theta_range = (-.99, -.49)
            self.est_theta = -.74
        else:
            self.risk_preference = "Wrong input"
        return self.risk_preference


    @directive_decorator("returned_response")
    def returned_response(self, message: Message):
        '''records the response of the agent'''

        payload = message.get_payload()
        response = (payload["choice"][0]) #reset every choice everytime
        #print(response)

        self.collect_data(response) # collect data and calculate payoff



    def collect_data(self, response):
        '''collect data and send lottery payoff to agents'''

        random_int = random.uniform(0, 1)  # a winning float from 0 to 1
        first = response[0]  # tuple of 1st choice
        second = response[1]
        if random_int < first[0]:  # choice 1 is chosen
            response.append(first[1])
        else:  # choice 2 is chosen
            response.append(second[1])

        outcome = response[2] #get outcome: A_x or B_x
        self.outcome_history.append(outcome)
        #print(self.outcome_history)

        numA = 0
        for choice in self.outcome_history:

            if 'A' in choice:
                numA += 1

        risk_preference = self.get_theta(int(numA))


        self.payoff_list.append(response[3]) #record payoffs of all played lottery

        if len(self.outcome_history) == 10: #make sure agent complete all lotteries
            print(self.outcome_history)
            print("completed rows:", len(self.payoff_list))
            print(self.risk_preference)
            x = random.randint(0,9)
            payload = {}
            payload["payoff"] = self.payoff_list[x] #randomly choose one played lottery
            message = Message()
            message.set_sender(self)
            message.set_directive("get payoff")
            message.set_payload(payload)
            self.send(self.agents[0], message)

            self.experiment_log({"subject id":self.agent_id, "choice" : self.outcome_history,
                                 "risk preference" : risk_preference, "est_theta" : self.est_theta,
                                 "theta_range": self.theta_range, "played lotteries payoff" : self.payoff_list,
                                 "payoff received" : self.payoff_list[x]})

