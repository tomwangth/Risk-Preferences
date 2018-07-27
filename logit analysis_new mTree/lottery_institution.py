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

        # >>>> data for the experiment <<<<
        self.experiment = None # to make sure it is changed
        self.run = None  # to make sure it is changed
        self.theta = None # theta for data
        self.delta = None # delta for data
        self.epsilon = None #epsilon for data
        self.error = None #realized delta
        self.choice_outcome = [] #actual outcome list, sent to experiment log
        self.outcome_history = {} #store all data
        self.payoff_list = [] #store payoffs



    @directive_decorator("fill_in_bundle")
    def fill_in_rows(self, message: Message):
        ''' puts in the rows into the bundles & set num of experiments/runs '''

        payload = message.get_payload()
        self.bundles = payload["bundle"]
        self.experiment = payload["experiment"]
        self.run = payload["run"]



    @directive_decorator("fill_in_agents")
    def fill_in_agents(self, message: Message):
        '''give agents to self'''

        payload = message.get_payload()
        self.agents = payload["agents"]



    @directive_decorator("theta_delta")
    def theta_delta(self, message: Message):
        '''keep track of agent's theta, delta'''

        payload = message.get_payload()
        self.theta = payload["theta"]
        self.delta = payload["delta"]
        self.epsilon = payload["epsilon"]



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


    @directive_decorator("returned_response")
    def returned_response(self, message: Message):
        '''records the response of the agent'''

        payload = message.get_payload()
        response = (payload["choice"][0]) #reset every choice everytime

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


        outcome_list = response[2] #get outcome: A_x or B_x

        if self.experiment not in self.outcome_history.keys():
            self.outcome_history[self.experiment] = {}
        if self.run not in self.outcome_history[self.experiment].keys():
            self.outcome_history[self.experiment][self.run] = []

        temp_round_list = self.outcome_history[self.experiment][self.run]
        temp_round_list.append(outcome_list)
        temp_round_list = temp_round_list[0:10]
        self.outcome_history[self.experiment][self.run] = temp_round_list


        #keep track of num experiments/runs
        print("next row of lotteries")
        print(self.experiment)
        print(self.run)
        print("agent making choice...")


        if len(temp_round_list) == 10: #make sure it stops at the end of list
            '''collect data, send results to experiment logs'''

            print("Outcome in this run:", temp_round_list)
            self.outcome = temp_round_list
            self.choice_outcome = [self.experiment, self.run, self.theta, self.delta, self.outcome, self.epsilon]
            self.experiment_log([self.experiment, self.run, self.theta, self.delta,  self.outcome, self.epsilon])
            self.outcome_history = {} # reset outcome_history

            #w = csv.writer(open("Holt_Laury_Output raw2.csv", "a"))
            #w.writerow(self.choice_outcome)

        self.choice_outcome = [] #reset choice_outcome


        self.payoff_list.append(response[3]) #record payoffs of all played lottery

        if len(temp_round_list) == 10: #make sure agent complete all lotteries
            '''send payoff to the agents'''

            print("completed rows:", len(self.payoff_list))
            x = random.randint(0,9)
            payload = {}
            payload["payoff"] = self.payoff_list[x] #randomly choose one played lottery
            message = Message()
            message.set_sender(self)
            message.set_directive("get payoff")
            message.set_payload(payload)
            self.send(self.agents[0], message)
            self.payoff_list = []


