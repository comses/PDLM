#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 06-21-25 
#

import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Convert to string and pretty print
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
        
def parse_and_save_model_atomic(model_text, output_filename):
    # Initialize the root XML element
    root = ET.Element("statechart:Model", {
        "xmi:version": "2.0",
        "xmlns:xmi": "http://www.omg.org/XMI",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:statechart": "http://statechart/1.0"
    }) 

    # Collecting States
    states = []
    state_patterns = re.finditer(r'(InitialState|State|FinalState)\s*{([^}]*)}', model_text, re.DOTALL)
    for match in state_patterns:
        state_type = match.group(1)
        state_content = match.group(2).strip()

        state_data = {'Type': state_type}
        name_match = re.search(r'Name\s*=\s*"([^"]+)"', state_content)
        if name_match:
            state_data['Name'] = name_match.group(1)

        
        if 'OutputFunction' in state_content:
            output_function = {}
            for field in ['Action', 'Description', 'Guard', 'Message', 'OutputPort']:
                field_match = re.search(rf'{field}\s*=\s*"([^"]*)"', state_content)
                if field_match:
                    output_function[field] = field_match.group(1)
            state_data['OutputFunction'] = output_function

        states.append(state_data)
    # print(states

    transitions = []
    transition_patterns = re.finditer(r'(Transition|InternalTransition|ExternalTransition)\s*{(.*?)}', model_text, re.DOTALL)
    for match in transition_patterns:
        transition_type = match.group(1)
        transition_content = match.group(2).strip()

        transition_data = {'Type': transition_type}
        fields = [
            ('Action', r'Action\s*=\s*\"([^\"]+)\"'),
            ('Description', r'Description\s*=\s*\"([^\"]+)\"'),
            ('Source', r'Source\s*=\s*\"([^\"]+)\"'),
            ('Target', r'Target\s*=\s*\"([^\"]+)\"'),
            ('TimeAdvanceType', r'TimeAdvanceType\s*=\s*(\w+)'),
            ('TimeAdvanceValue', r'TimeAdvanceValue\s*=\s*([0-9]+\.?[0-9]*)'),
            ('Guard', r'Guard\s*=\s*\"([^\"]*)\"'),
            ('InputPort', r'InputPort\s*=\s*\"([^\"]+)\"'),
            ('Message', r'Message\s*=\s*\"([^\"]+)\"')
        ]

        for field, pattern in fields:
            match = re.search(pattern, transition_content)
            if match:
                transition_data[field] = match.group(1)

        transitions.append(transition_data)
    print(transitions)

    
    # XML root setup
    root = ET.Element('statechart:Model', attrib={
        'xmi:version': '2.0',
        'xmlns:xmi': 'http://www.omg.org/XMI',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns:statechart': 'http://statechart/1.0'
    })

    # Track states for reference
    state_refs = {}

    # Add states
    for i, state in enumerate(states):
        if state['Type'] == 'InitialState':
            elem = ET.SubElement(root, 'initialState', Name=state['Name'], Description='', outgoing=f"//@transitions.{i}")
            state_refs[state['Name']] = f"//@initialState"
        elif state['Type'] == 'FinalState':
            elem = ET.SubElement(root, 'finalState', Name=state['Name'])
            state_refs[state['Name']] = f"//@states.{i-1}"
        else:
            elem = ET.SubElement(root, 'states', attrib={
                'xsi:type': 'statechart:State',
                'tag': f"//@states.{i-1}",
                'Name': state['Name']
            })
            if 'OutputFunction' in state:
                output = ET.SubElement(elem, 'outputFunctions', OutputPort=state['OutputFunction']['OutputPort'])
                ET.SubElement(output, 'Message').text = state['OutputFunction']['Message']
                ET.SubElement(output, 'Action').text = state['OutputFunction']['Action']
            state_refs[state['Name']] = f"//@states.{i-1}"

    # Add transitions
    for i, trans in enumerate(transitions):
        if trans['Type'] == 'Transition':
            attrib={
                'xsi:type': f"statechart:{trans['Type']}",
                'source': state_refs.get(trans['Source'], ''),
                'target': state_refs.get(trans['Target'], '')
            }
        elif trans['Type'] == 'ExternalTransition':
            attrib={
                'xsi:type': f"statechart:{trans['Type']}",
                'TimeAdvanceType': trans['TimeAdvanceType'],
                'TimeAdvanceValue': trans['TimeAdvanceValue'],
                'source': state_refs.get(trans['Source'], ''),
                'target': state_refs.get(trans['Target'], ''),
                'InputPort': trans['InputPort'],
            }
        else:
            attrib={
                'xsi:type': f"statechart:{trans['Type']}",
                'TimeAdvanceType': trans['TimeAdvanceType'],
                'TimeAdvanceValue': trans['TimeAdvanceValue'],
                'source': state_refs.get(trans['Source'], ''),
                'target': state_refs.get(trans['Target'], ''),
            }

        trans_elem = ET.SubElement(root, 'transitions', attrib)
       
        if 'Action' in trans:
            action_list = trans['Action'].split(',')
            for action in action_list:
                ET.SubElement(trans_elem, 'Action').text = action
        if 'Guard' in trans:
            guard_list = trans['Guard'].split(',')
            for guard in guard_list:
                ET.SubElement(trans_elem, 'Guard').text = guard
        if 'Message' in trans:
            ET.SubElement(trans_elem, 'Message').text = trans['Message']

    xml_output = prettify(root)

    # Save to file with proper formatting
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(xml_output)

def parse_and_save_model_coupled(model_text, output_filename):

    # Pattern to match Coupling
    coupling_pattern = r'Coupling\s*{\s*M1Name = "(?P<m1_name>.*?)"\s*M1Port = "(?P<m1_port>.*?)"\s*M2Name = "(?P<m2_name>.*?)"\s*M2Port = "(?P<m2_port>.*?)"\s*}'

    # Dictionary to store the parsed data
    model_dict = {
        # 'AtomicModelList': [],
        'CouplingList': []
    }

    couplings = re.findall(coupling_pattern, model_text, re.DOTALL)
    for coupling in couplings:
        model_dict['CouplingList'].append({
            'M1Name': coupling[0],
            'M1Port': coupling[1],
            'M2Name': coupling[2],
            'M2Port': coupling[3]
        })
    print(model_dict['CouplingList'])

    # Create root XML element
    root = ET.Element("model")
    composite_model = ET.SubElement(root, "compositeModel", name = "CoupledModel")

    for coupling in model_dict['CouplingList']:
        ET.SubElement(composite_model, "coupling", m1name=coupling['M1Name'], m1port=coupling['M1Port'], m2name=coupling['M2Name'], m2port=coupling['M2Port'])
    
    xml_output = prettify(root) 
    # Save to file with proper formatting
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(xml_output)    

def parse_and_save_model_with_error_handling_atomic(model_text, output_filename="model_output.xml"):
    try:
        # Try parsing the model text into XML format
        parse_and_save_model_atomic(model_text, output_filename)
        return None
    
    except Exception as e:
        # Catch and display any errors encountered during parsing or saving
        print(f"Failed to parse and save the model. Error: {str(e)}")

        return str(e)

def parse_and_save_model_with_error_handling_coupled(model_text, output_filename="model_output.xml"):
    try:
        # Try parsing the model text into XML format
        parse_and_save_model_coupled(model_text, output_filename)
        return None
    
    except Exception as e:
        # Catch and display any errors encountered during parsing or saving
        print(f"Failed to parse and save the model. Error: {str(e)}")

        return str(e)

##--------------------------------------------------------------------------------------------------
# Example usage:
model_text = """
Model {
    ConfluentType = FIT

    // States
    InitialState { Name = "start" }

    State { 
        Name = "off"
        OutputFunction {
            Action = ""
            Description = "Output Function for state off"
            Guard = "" 
            Message = "off" 
            OutputPort = "signal_out"
        }
    }

    State { 
        Name = "on"
        OutputFunction {
            Action = ""
            Description = "Output Function for state on"
            Guard = "" 
            Message = "on" 
            OutputPort = "signal_out"
        }
    }

    // Transitions
    Transition {  
        Action = "state.toggle(), time_advance.set(1)"
        Description = "Toggling state from off to on and setting time_advance"
        Source = "off"  
        Target = "on" 
        TimeAdvanceType = Value
        TimeAdvanceValue = 1.0
    }

    Transition {  
        Action = "state.toggle(), time_advance.set(1)"
        Description = "Toggling state from on to off and setting time_advance"
        Source = "on"  
        Target = "off" 
        TimeAdvanceType = Value
        TimeAdvanceValue = 1.0
    }
}
"""

# Example input
coupled_model_text = '''
Coupled Model {
    AtomicModelList {
        AtomicModel {
            Name = "controller"
            InPortList {
            }
            OutPortList {
                OutPort { Name = "toggle_out" }
            }
        }
        AtomicModel {
            Name = "light"
            InPortList {
                InPort { Name = "toggle_in" }
            }
            OutPortList {
            }
        }
    }
    CouplingList {
        Coupling {
            M1Name = "controller"
            M1Port = "toggle_out"
            M2Name = "light"
            M2Port = "toggle_in"
        }
    }
}
'''
##--------------------------------------------------------------------------------------------------

# parse_and_save_model_with_error_handling_coupled(coupled_model_text, './out.xml')