# Basic Includes
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container

# Includes needed to send the class objects to be instantiated in the actor system
from lottery_agent import BasicAgent
from lottery_envrionment import BasicEnvironment
from lottery_institution import BasicInstitution
import random as rnd

print("Based on Holt Laury, you will get your rewards and risk preferences parameter")

# instantiating the container
container = Container()
# creating a root environment. For the purposes of this experiment, it's just the containing environment
container.create_root_environment(BasicEnvironment)
# creating a single institution for this experiment
container.setup_environment_institution(BasicInstitution)
# create agent for the purposes of the experiment
container.setup_environment_agents(BasicAgent, 1)


#makes the bundle in environment
message = Message()
message.set_sender("external")
message.set_directive("create_bundle")
payload = {}
payload["reward_A_1"] = 1.00 # sets the reward for all of the choices
payload["reward_A_2"] = 0.80
payload["reward_B_1"] = 1.93
payload["reward_B_2"] = .05
payload["num_rows"] = 10 #sets the number of rows
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
payload["agent_id"] = "513"
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
