import os
import re
from collections import defaultdict

class UML_Statechart_generator:
    def __init__(self) -> None:
        return None
    
    def block_to_json(self, block: str):
        # Remove the "Transition {" and ending "}"
        content = block.strip().removeprefix("Transition").strip().lstrip("{").rstrip("}")
        
        result = {}
        # Match lines like: Key = "value" or Key = value
        pattern = re.compile(r'(\w+)\s*=\s*("[^"]*"|\S+)')
        for match in pattern.finditer(content):
            key, value = match.groups()
            if value.startswith('"') and value.endswith('"'):
                result[key] = value.strip('"')
            elif value.lower() == "infinity":
                result[key] = float('inf')
            else:
                try:
                    result[key] = float(value) if '.' in value else int(value)
                except ValueError:
                    result[key] = value  # fallback to string if conversion fails
        
        return result

    def parse_block(self, block: str):
        """
        Recursively parse a DSL block into a dictionary.
        Handles repeated nested blocks by storing them in a list.
        """
        block = block.strip().strip("{}").strip()
        result = {}
        lines = []
        nested = None
        nested_name = ""
        nested_blocks = defaultdict(list)

        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            if "{" in line and "}" not in line:
                # Start of nested block
                nested_name = line.split()[0]
                nested = []
            elif "}" in line and nested is not None:
                # End of nested block
                nested_block = "\n".join(nested)
                nested_blocks[nested_name].append(self.parse_block(nested_block))
                nested = None
            elif nested is not None:
                nested.append(line)
            else:
                # Regular key = value line
                match = re.match(r'(\w+)\s*=\s*("[^"]*"|\S+)', line)
                if match:
                    key, value = match.groups()
                    if value.startswith('"') and value.endswith('"'):
                        result[key] = value.strip('"')
                    elif value.lower() == "infinity":
                        result[key] = float('inf')
                    else:
                        try:
                            result[key] = float(value) if '.' in value else int(value)
                        except ValueError:
                            result[key] = value

        # Add all nested blocks, collapsing singletons
        for key, blocks in nested_blocks.items():
            result[key] = blocks if len(blocks) > 1 else blocks[0]
        return result

    def extract_state_blocks(self, text: str):
        """
        Extracts all top-level State { ... } blocks.
        """
        pattern = re.compile(r'\bState\s*{(?:[^{}]*{[^{}]*})*[^}]*}', re.DOTALL)
        return pattern.findall(text)

    def translate(self, sc: str):
        print("Translating into StateChart Diagram")
        sc_dgm = "@startuml\nhide empty description\n" ##Starting the UML State Diagram##

        # For Initialization
        pattern = re.compile(r'\bTransition\s*{[^{}]*}', re.DOTALL)
        transitions = pattern.findall(sc)
        for i, block in enumerate(transitions, 1):
            block_json = self.block_to_json(block)

            if block_json["TimeAdvanceType"] == float('inf'):
                sc_dgm += f"""[*] -[dotted]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", TA = "Infinity"\n"""
            else:
                sc_dgm += f"""[*] -[dotted]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", TA = "{block_json["TimeAdvanceValue"]}"\n"""

        # For External Transition
        pattern = re.compile(r'\bExternalTransition\s*{[^{}]*}', re.DOTALL)
        transitions = pattern.findall(sc)
        for i, block in enumerate(transitions, 1):
            block_json = self.block_to_json(block)
            
            if block_json["TimeAdvanceType"] == float('inf'):
                sc_dgm += f""""{block_json["Source"]}" -[bold]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", G = "{block_json["Guard"]}", IP = "{block_json["InputPort"]}", M = "{block_json["Message"]}", TA = "Infinity"\n"""
            else:
                sc_dgm += f""""{block_json["Source"]}" -[bold]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", G = "{block_json["Guard"]}", IP = "{block_json["InputPort"]}", M = "{block_json["Message"]}", TA = "{block_json["TimeAdvanceValue"]}"\n"""

        # For Internal Transition
        pattern = re.compile(r'\bInternalTransition\s*{[^{}]*}', re.DOTALL)
        transitions = pattern.findall(sc)
        for i, block in enumerate(transitions, 1):
            block_json = self.block_to_json(block)
            
            if block_json["TimeAdvanceType"] == float('inf'):
                sc_dgm += f""""{block_json["Source"]}" -[dashed]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", G = "{block_json["Guard"]}", TA = "Infinity"\n"""
            else:
                sc_dgm += f""""{block_json["Source"]}" -[dashed]-> "{block_json["Target"]}" : A = "{block_json["Action"]}", G = "{block_json["Guard"]}", TA = "{block_json["TimeAdvanceValue"]}"\n"""

        # For States

        states = self.extract_state_blocks(sc)

        for state in states:

            if 'outputfunction' in state.lower():
                name = state.split('Name = "')[1].split('"')[0]
                of_blocks = self.parse_block(state)
                
                if isinstance(of_blocks['OutputFunction'], list):
                    for of in of_blocks['OutputFunction']:
                        sc_dgm += f""""{name}" : OF $ A = "{of['Action']}", G = "{of['Guard']}", M = "{of['Message']}", OP = "{of['OutputPort']}"\n"""
                else:
                    of = of_blocks['OutputFunction']
                    sc_dgm += f""""{name}" : OF $ A = "{of['Action']}", G = "{of['Guard']}", M = "{of['Message']}", OP = "{of['OutputPort']}"\n"""

        sc_dgm += "@enduml"
        return sc_dgm