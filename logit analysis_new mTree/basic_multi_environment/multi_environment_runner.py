# Basic Includes
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.multi_container import MultiContainer

# Includes needed to send the class objects to be instantiated in the actor system
from basic_agents.basic_agent import BasicAgent
from basic_agents.basic_envrionment import BasicEnvironment
from basic_agents.basic_institution import BasicInstitution

print("This is an example of a very simple agent experiment")

# instantiating the container
container = MultiContainer()

def startup_environment(name):
    # creating a root environment. For the purposes of this experiment, it's just the containing environment
    container.create_environment(BasicEnvironment, name)
    # creating a single institution for this experiment
    container.setup_environment_institution(name, BasicInstitution)
    # create some number of agents for the purposes of the experiment
    container.setup_environment_agents(name, BasicAgent, 1)

    # a basic initialization example. This will be processed by the environment and possibly distributed from there
    message = Message()
    message.set_sender("external")
    message.set_directive("initialize_boxes")
    container.send_root_environment_message(name, message)

    # a message that the environment will route to startup agents in the experiment
    message = Message()
    message.set_sender("external")
    message.set_directive("start_agents")
    container.send_root_environment_message(name, message)


startup_environment("test1")
startup_environment("test2")
startup_environment("test3")
