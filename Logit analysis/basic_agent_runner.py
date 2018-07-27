# Basic Includes
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container

# Includes needed to send the class objects to be instantiated in the actor system
from basic_agent import BasicAgent
from basic_envrionment import BasicEnvironment
from basic_institution import BasicInstitution
import random as rnd

print("This is the test cases for a holt-laury agent")

# instantiating the container
container = Container()
# creating a root environment. For the purposes of this experiment, it's just the containing environment
container.create_root_environment(BasicEnvironment)
# creating a single institution for this experiment
container.setup_environment_institution(BasicInstitution)
# create some number of agents for the purposes of the experiment
container.setup_environment_agents(BasicAgent, 1)


num_monte_trials = 10
num_experiments = 100 #input m numbers of experiments
num_runs = 10  # input num runs/subjects, each subject comes in with a different theta

delta_list = []

for i in range(num_monte_trials):
    x = round(rnd.uniform(0, 0.5), 2)
    delta_list.append(x)
    x = None
print(delta_list)

#delta_list = [0.1,0.2,0.3,0.4] #input delta for monte carlo trials, each trial has a fixed delta


for delta in delta_list: # first loop for monte

    for m in range(num_experiments): #second loop for m experiment

        theta_list = []

        for i in range(num_runs):
            x = round(rnd.uniform(-0.15, 0.68), 2)
            theta_list.append(x)
            x = None

        run = 0

        for theta in theta_list: #third loop for runs

            run += 1
            epsilon = round(rnd.uniform(-0.3,0.3),2)

            print("Experiment:",m,"Run:", num_runs)

            #makes the bundle in environment
            message = Message()
            message.set_sender("external")
            message.set_directive("initialize_rows")
            payload = {}
            payload["reward_A_1"] = 2 # sets the reward for all of the choices
            payload["reward_A_2"] = 1.60
            payload["reward_B_1"] = 3.85
            payload["reward_B_2"] = .1
            payload["num_rows"] = 10 #sets the number of rows
            payload["experiment"] = m # what period the experiment is on
            payload["total_experiments"] = num_experiments
            payload["run"] = run
            payload["total_runs"] = num_runs
            print(payload["run"])
            message.set_payload(payload)
            container.send_root_environment_message(message)

            #sends the bundle from the envir. to the institution
            message = Message()
            message.set_sender("external")
            message.set_directive("send_bundle")
            container.send_root_environment_message(message)

            # setup the agents with theta and sd
            message = Message()
            message.set_sender("external")
            message.set_directive("initialize_agents")
            payload = {}
            payload["theta"] = theta
            payload["delta"] = delta # must be positive or 0
            payload["epsilon"] = epsilon
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

            # start the experiment
            message = Message()
            message.set_sender("external")
            message.set_directive("start_experiment")
            container.send_root_environment_message(message)

        #collects the rounds data in the environment
        message = Message()
        message.set_sender("external")
        message.set_directive("collect_data")
        container.send_root_environment_message(message)

    print("Done")