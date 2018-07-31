from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container

from box_search.search_agent import SearchAgent
from box_search.search_envrionment import SearchEnvironment
from box_search.search_institution import SearchInstitution

print("This is an example of a very simple search experiment")

###
# Step 1: Initialize the basic experiment container
###
container = Container()
container.create_root_environment(SearchEnvironment)
container.setup_environment_institution(SearchInstitution)
container.setup_environment_agents(SearchAgent, 1)

###
# Step 2: Initialize the round... tell environment to let agents and institutions to know about each other
###
message = Message()
message.set_sender("external")
message.set_directive("initialize_round")
container.send_root_environment_message(message)
print("should have initialized")
###
# Step 3: Initialize the boxes for search at the environment and institution
###
message = Message()
message.set_sender("external")
message.set_directive("initialize_boxes")
box_list = [1,2,3,4,5]
payload = {}
payload["box_list"] = box_list
message.set_payload(payload)
container.send_root_environment_message(message)

###
# Step 4: Alert the institution to start the round
###
message = Message()
message.set_sender("external")
message.set_directive("start_round")
message.set_payload(payload)
container.send_root_environment_message(message)


