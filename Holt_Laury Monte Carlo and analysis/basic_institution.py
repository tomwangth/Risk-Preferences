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
        self.response = []
        self.outcome = [] # the outcome of the agent's choice

        self.experiment = None # to make sure it is changed

        #>>>>>>>>>>>>>>>>>>>  Everything below is for storing data  <<<<<<<<<<<<<<

        self.theta = None # theta for data
        self.delta = None # sd for data
        self.epsilon = None
        #self.all_data = {} # stores all of the data for all of the periods
        self.total_experiments = None # total number of pairs
        self.run =  None
        self.choice_outcome = [] #actual outcome list, written in csv file
        self.outcome_list = None
        self.outcome_history = {}
        self.total_run = None # total number of round


    @directive_decorator("fill_in_rows")
    def fill_in_rows(self, message: Message):
        ''' puts in the rows into the bundles + set period '''
        payload = message.get_payload()
        self.bundles = payload["bundle"]
        self.experiment = payload["experiment"]
        self.total_experiments = payload["total_experiments"]
        self.run = payload["run"]
        self.total_runs = payload["total_runs"]



    @directive_decorator("fill_in_agents")
    def fill_in_agents(self, message: Message):
        '''give agents to self'''

        payload = message.get_payload()
        self.agents = payload["agents"]


    @directive_decorator("theta_sd")
    def theta_sd(self, message: Message):
        '''gives theta and sd to self '''


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
            #print(self.experiment)
            #print(self.run)
            #print(self.bundles)
            #print("bundles #",len(self.bundles))
            for row in self.bundles:
                payload= {}
                payload["row"] = row
                message = Message()
                message.set_sender(self)
                message.set_directive("make_choice")
#TO DO watch out for message cuing
                message.set_payload(payload)
                self.send(agent,message)

                message2 = Message()
                message2.set_sender(self)
                message2.set_directive("grab_response")
                self.send(self.agents[0],message2)

    @directive_decorator("returned_response")
    def returned_response(self, message: Message):


        ''''records the response of the agent'''

        payload = message.get_payload()
        response = (payload["choice"][0]) #reset every choice everytime
        #print(response) #check here


        self._outcome(response) # calculates which payout is chosen



    def _outcome(self, response):
        '''calcualtes the payoff of the agents choice'''



        #print(self.experiment)
        random_int = random.uniform(0,1) # a winning float from 0 to 1

        first = response[0] #tuple of 1st choice
        second = response[1]



        if random_int < first[0]: # choice 1 is chosen
            response.append(first[1])

        else:                     # choice 2 is chosen
            response.append(second[1])


        outcome_list = response[2] #get outcome: A_x or B_x

        #print((self.outcome_history).keys())
        if self.experiment not in self.outcome_history.keys():
            self.outcome_history[self.experiment] = {}
            print("Alex")
        if self.run not in self.outcome_history[self.experiment].keys():
            self.outcome_history[self.experiment][self.run] = []

        temp_round_list = self.outcome_history[self.experiment][self.run]
        #print(temp_round_list)
        #print(outcome_list)
        #print(self.outcome_history[self.experiment])
        temp_round_list.append(outcome_list)
        temp_round_list = temp_round_list[0:10]
        self.outcome_history[self.experiment][self.run] = temp_round_list
        print(temp_round_list)






        print("*****")
        print(self.experiment)
        print(self.run)
        print(outcome_list)
        print(self.outcome_history)
        print("^^^^^^")



        message = Message()

        message.set_sender(self)
        message.set_directive("send_data")
        payload = {}
        # self.outcome.append("None")
        # payload["bundle_response"] = self.outcome

        message.set_payload(payload)

        #make sure it stops at the end of list
        if "B_10" in temp_round_list:

            #print(temp_round_list)
            self.outcome = temp_round_list
            self.choice_outcome = [self.experiment, self.run, self.theta, self.delta, self.outcome, self.epsilon]
            #print(self.choice_outcome)

            self.outcome_history = {}


            w = csv.writer(open("Holt_Laury_Output raw2.csv", "a")) # run the same experiment
            w.writerow(self.choice_outcome)
            # print(self.choice_outcome)
        self.choice_outcome = [] #reset choice_outcome


