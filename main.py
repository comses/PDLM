#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Dr. Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 10-26-2025 
# 

from seg import *
import json

test_path ="testcases.json"

with open(test_path, "r", encoding="utf-8") as file:
    data = json.load(file)

comp = "CarWash"

pdevs_facts = SEG(data[comp], comp, engine = 'openai', model= 'gpt-4o-mini')

generate_statecharts(comp, pdevs_facts)