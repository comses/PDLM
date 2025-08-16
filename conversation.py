#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 06-21-25 
#

import os
import json
import re
import openai
from utils import *
import config

openai.api_version = config.OPENAI_API_VERSION
openai.api_type = config.OPENAI_API_TYPE
openai.api_base = config.OPENAI_API_BASE
openai.api_key = config.OPENAI_API_KEY

class GPTAgent:
    def __init__(self, system_prompt="You are a helpful AI assistant. Provide clear, concise, and insightful responses."):
        """Initialize the GPT agent with a fixed system prompt and conversation history."""
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        
    def ask(self, user_input):
        """Send a message to the GPT agent and return the response."""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=self.conversation_history,
            temperature=0.7, 
        )
        
        assistant_reply = response["choices"][0]["message"]["content"]
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply, self.conversation_history

class Conversation:
    with open("./Grammar_prompts/primer-fact-extractor.md", 'r') as f:
        lines = f.readlines()
    FIRST_STAGE_PRIMER = ''.join(lines[7:])

    with open("./Grammar_prompts/PDEVS-Spec atomic formation.md", 'r') as f:
        lines = f.readlines()
    PDEVS_SPEC_GRAMMAR = ''.join(lines[7:])
    
    with open("./Grammar_prompts/PDEVS-Spec coupled formation.md", 'r') as f:
        lines = f.readlines()
    COUPLED_PDEVS_SPEC = ''.join(lines[7:])
    
    SPECIFIER_MESSAGE_TEMPLATE = """### USER REQUEST
Now produce a PDEVS specification in the requested TOML-like language respecting the following statements:\n"""

    def __init__(
        self,
        temperature: float | tuple[float, float] = 0.5,
    ) -> None:
        self.concept_temperature = temperature

    def coupled_facts_extractor(self, message: str):
        pattern = re.compile(r'coupled model: ([\s\S]*?)(?=\n#)', re.MULTILINE)
        matches = pattern.findall(str(message).lower())
        # Convert list to dictionary
        coupled_model_dict = {}
        for entry in matches:
            key, value = entry.split('\n', 1)  # Split on the first newline
            coupled_model_dict[key.strip()] = value.strip()
        
        # return matches[0]
        return coupled_model_dict

    def atomic_facts_extractor(self, message: str):
        pattern = re.compile(r'atomic model: ([\s\S]*?)(?=\n#)', re.MULTILINE)

        matches = pattern.findall(str(message).lower())

        # Convert list to dictionary
        atomic_model_dict = {}
        for entry in matches:
            key, value = entry.split('\n', 1)  # Split on the first newline
            atomic_model_dict[key.strip()] = value.strip()
        
        return atomic_model_dict

    def user_interact(self, output_dir, message: str) -> str:

        messages = [
            {"role": "system", "content": self.FIRST_STAGE_PRIMER},
            {"role": "user", "content": message},
        ]
        print("GENERATING FACTS")
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini", messages=messages, temperature=self.concept_temperature
        )
        complete_facts = completion.choices[0].message["content"]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_dir + '/full_facts.txt', "w", encoding='utf-8') as file:
            file.write(complete_facts)
        
        # user_check = input("Can we proceed with the extracted facts?: ")
        # if 'yes' in user_check.lower():
        complete_facts = open(output_dir + '/full_facts.txt').read()
        coupled_facts = self.coupled_facts_extractor(complete_facts)
        atomic_dict = self.atomic_facts_extractor(complete_facts)
    
        print('------------------------------------------------------------------------')
        print("GENERATING STATECHARTS FOR ATOMIC COMPONENTS")

        ##Initializing the Agent. 
        Atomic_Generator_Agent = GPTAgent(system_prompt=self.PDEVS_SPEC_GRAMMAR)
        Coupled_Generator_Agent = GPTAgent(system_prompt=self.COUPLED_PDEVS_SPEC)
        final_atomic_dict = {}
        for atomic in atomic_dict.keys():
            atomic_facts = atomic_dict[atomic]
            print(atomic_facts)
            print("*********************************************************")
            check = True
            user_modifications = None
            parsing_error = None
            while check:
                if user_modifications: 
                    msg = f"current version:\n\n{atomic_facts}\n\nmodifications_requested: {user_modifications}."
                    
                elif parsing_error: 
                    msg = f"current version:\n\n{atomic_facts}\n\nError occured while parsing into XML schema: {parsing_error}."

                else:
                    msg = f"The overall system facts:\n\n{complete_facts}\n\nCreated atomic models:{final_atomic_dict}\n\nFacts for atomic model to be created:\n\n{atomic_facts}.\n\nMake sure to use relevant inport and outports to establish the proper connectivity in the coupled models."
                    
                atomic_spec, conv = Atomic_Generator_Agent.ask(msg)

                print(atomic_spec)
                ## User check 
                user_check = input("Do you want to make any changes or comments on these specifications? (Type 'yes' to modify, 'no' to accept, or write your comments): ")

                if user_check.lower() == "yes":
                    with open('./modifications.md', 'r', encoding='utf-8') as file:
                        user_modifications = file.read()
                        continue
                else:
                    user_modifications = None

                    if not os.path.exists(output_dir):
                        os.mkdir(output_dir)
                    with open(output_dir + f'/{atomic}_facts.txt', "w", encoding='utf-8') as file:
                        file.write(atomic_facts)
                    with open(output_dir + f'/{atomic}_statechart.txt', "w", encoding='utf-8') as file:
                        file.write(atomic_spec)

                    parsing_error = parse_and_save_model_with_error_handling_atomic(atomic_spec, output_dir + f"/{atomic}.xml")
                    if parsing_error:
                        continue
                check = False
            
            final_atomic_dict[atomic] = atomic_spec
        print('------------------------------------------------------------------------')
        with open(output_dir + '/conversation.txt', "w", encoding='utf-8') as file:
            file.write("\n".join(json.dumps(entry, indent=4) for entry in conv))

        print("GENERATING COUPLE MODELS")
        final_coupled_dict = {}
        for coupled in coupled_facts:

            msg = f"The coupled model facts:\n\n{coupled}\n\nGenerated Atomic Model Specifications:\n\n{final_atomic_dict}\n\nGenerated Coupled Model Specifications:\n\n{final_coupled_dict}. Provide accurate couplings between the components mentioned in the coupled model facts."
            
            coupled_spec, _ = Coupled_Generator_Agent.ask(msg)
            print(coupled_spec)
            final_coupled_dict[coupled] = coupled_spec
            
            with open(output_dir + f'/{coupled}_specification.txt', "w", encoding='utf-8') as file:
                file.write(coupled_spec)
            parse_and_save_model_with_error_handling_coupled(coupled_spec, output_dir + f"/{coupled}.xml")
        print('Created all the needed atomic shatecharts and coupled specifications')
