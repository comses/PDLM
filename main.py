#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 06-21-25 
#

from conversation import Conversation
import json

# Create an instance of the Conversation class
conversation = Conversation()

with open('./system_descriptions.json', 'r') as file: ## All the prompts discusssed in the paper are provided in the json file.
    data = json.load(file)

name = "example_1" ## Replace the system name. 
sys_des = data[f"{name}"] ## Replace the system description if testing on a different (than examples) system. 

output_dir = f'./Output/PDEVS_LLM/{name}'
conversation.user_interact(output_dir, sys_des) 