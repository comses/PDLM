from seg import *
import json

test_path ="testcases.json"

with open(test_path, "r", encoding="utf-8") as file:
    data = json.load(file)

comp = "CarWash"

pdevs_facts = SEG(data[comp], comp, engine = 'openai', model= 'gpt-4o-mini')

generate_statecharts(comp, pdevs_facts)