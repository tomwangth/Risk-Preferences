
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container

# Includes needed to send the class objects to be instantiated in the actor system
from lottery_agent import LotteryAgent
from lottery_envrionment import LotteryEnvironment
from lottery_institution import LotteryInstitution
import random as rnd

print("This is the monte carlo simulation for lottery choosing agents")

# instantiating the container
container = Container()
# creating a root environment. For the purposes of this experiment, it's just the containing environment
container.create_root_environment(BasicEnvironment)
# creating a single institution for this experiment
container.setup_environment_institution(BasicInstitution)
# create agent for the purposes of the experiment
container.setup_environment_agents(BasicAgent, 1)

'''This is the MES for Holt_Laury lotteries simulation, by changing the looping, num_experiment, num_runs, and epsilon, we can
have continuous/fixed theta, delta and epsilon''' #It is currently having continous delta and theta


'''run monte carlo experiment with continuous delta and theta'''

#num_monte_trials = 100 #input number of monte carlo trials
num_experiments = 100 #input m numbers of experiments
num_runs = 100  # input num runs/subjects, each subject comes in with a different theta

delta_list = []

#for i in range(num_monte_trials):
    #x = round(rnd.uniform(0, 0.5), 2)
    #delta_list.append(x)
    #x = None
#print(delta_list)

#for delta in delta_list: # k monte carlo trials with k delta

for m in range(num_experiments): #m experiments

    theta_list = []
    for i in range(num_runs):
        x = round(rnd.uniform(-0.15, 0.68), 2)
        theta_list.append(x)
        x = None

    run = 0
    for theta in theta_list: #p runs with continous thetas and delta
        delta = round(rnd.uniform(0, 0.5), 2)
        e = round(rnd.uniform(0,0.4),2)
        run += 1
        #epsilon = round(rnd.uniform(-e,e),2) #not using uniform anymore?
        print("epsilon:",e)

        print("Experiment:",m,"Run:", num_runs)

        #makes the bundle in environment
        message = Message()
        message.set_sender("external")
        message.set_directive("create_bundle")
        payload = {}
        # sets the reward for all of the choices
        payload["reward_A_1"] = 2
        payload["reward_A_2"] = 1.60
        payload["reward_B_1"] = 3.85
        payload["reward_B_2"] = .1
        payload["num_rows"] = 10 #sets the number of rows of lotteries
        payload["experiment"] = m # num of experiment is on
        payload["run"] = run
        message.set_payload(payload)
        container.send_root_environment_message(message)

        #sends the bundle from the envir. to the institution
        message = Message()
        message.set_sender("external")
        message.set_directive("send_bundle")
        container.send_root_environment_message(message)

        # setup the agents with theta and delta
        message = Message()
        message.set_sender("external")
        message.set_directive("initialize_agents")
        payload = {}
        payload["theta"] = theta
        payload["delta"] = delta  # parameter, must be positive or 0
        payload["epsilon"] = e  # parameter, must be positive or 0
        message.set_payload(payload)
        container.send_root_environment_message(message)

        #send agents from envir. to institution
        message = Message()
        message.set_sender("external")
        message.set_directive("send_agents")
        container.send_root_environment_message(message)

        #send list of institution to the agents
        message = Message()
        message.set_sender("external")
        message.set_directive("send_institution")
        container.send_root_environment_message(message)

        # start the experiment and collect data
        message = Message()
        message.set_sender("external")
        message.set_directive("start_experiment")
        container.send_root_environment_message(message)

print("\n")
print("Done")
