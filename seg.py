from llm_utils import *
from PL_utils import *
from sc_translate import *
import os

def generate_statecharts(comp, pdevs_facts):
    ## Initializing the Agent.
    PDEVS_ATOMIC_GRAMMAR = open("./Prompts/DEVS-Spec atomic statechart.md").read()

    Atomic_Generator_Agent = LLMAgent_no_json(system_prompt=PDEVS_ATOMIC_GRAMMAR, engine='openai', model='gpt-4.1')
    statechart = Atomic_Generator_Agent.ask(f"Generate PDEVS statechart for {comp}, given these PDEVS specifications:\n\n{pdevs_facts}")

    os.makedirs(f"./Results/{comp}", exist_ok=True)
    print("==========================================================")
    print("==========================================================")
    with open(f"./Results/{comp}/statechart.txt", "w", encoding="utf-8") as f:
        f.write(statechart)
    
    sc_translator = UML_Statechart_generator()
    statechart_plantuml = sc_translator.translate(statechart)

    with open(f"./Results/{comp}/statechart_plantuml.txt", "w", encoding="utf-8") as f:
        f.write(statechart_plantuml)
    print("The statecharts are saved in the Results folder")

def SEG(sys_des, comp, engine = 'openai', model = 'gpt-4o-mini'):

    props = props_extractor(sys_des, engine='openai', model='gpt-4o-mini')

    FIRST_STAGE_PRIMER = open("./Prompts/conceptual knowledge atomic.md").read()
    Facts_Generator_Agent = LLMAgent(system_prompt= FIRST_STAGE_PRIMER, engine=engine, model=model)
    pdevs_facts = Facts_Generator_Agent.ask(f"- SYSTEM DESCRIPTION:\n\n{sys_des}\n\n-ATOMIC COMPONENET: {comp}\n\n- GENERATED FACTS:\n")
    fin_pdevs_facts = pdevs_facts
    print(json.dumps(pdevs_facts, indent=4))
    bc= key_conditions_generator(message = sys_des, component = comp, engine = 'openai', model = 'gpt-4o-mini')
    print(json.dumps(bc, indent=4))
    PL_statements = PL_conversion_pdevs(pdevs_facts, component = comp, props = props, engine='openai', model='gpt-4o-mini')
    print(json.dumps(PL_statements, indent=4, ensure_ascii=False))
    bc_PL_statements = PL_conversion_bc(props, bc, engine='openai', model='gpt-4o-mini')
    print(json.dumps(bc_PL_statements, indent=4, ensure_ascii=False))

    lookup_dict = {
        "internal transition function" : "internal behavior",
        "external transition function" : "external behavior",
        "output function" : "output behavior"
    }

    en_check_dict = {
        "internal transition function" : False,
        "external transition function" : False,
        "output function" : False
    }

    min_unentail_conds_cnt = 9999
    
    ## Satisfiability check for the conditions.
    for m in range(3):
        conds = []
        for function in lookup_dict:
        
            conds_dict = bc_PL_statements[lookup_dict[function]]
            for idx in conds_dict:
                conds.append(conds_dict[idx][1])
        pl_conds, conds_sat = check_satisfiability(conds)
        
        if not conds_sat:
            print("Satisfiability check for the behavioral conditions failed. Would you like to manually modify the plausible facts?")
            bc = key_conditions_generator(message = sys_des, component = comp, engine = 'openai', model = 'gpt-4o-mini')
            print(json.dumps(bc, indent=4, ensure_ascii=False))
            bc_PL_statements = PL_conversion_bc(props, bc, engine='openai', model='gpt-4o-mini')
            print(json.dumps(bc_PL_statements, indent=4, ensure_ascii=False))
        else:
            print("Satisfiability check for the behavioral conditions passed")
            break

    # Self-Correction Loop
    for en_chk_cnt in range(3):

        unentail_conds_cnt = 0
        print(f"Entailment Check - {en_chk_cnt+1}")

        ## Satisfiability check for the facts.
        for n in range(3):
            facts = []
            for function in lookup_dict:
                facts_dict = PL_statements["Logical Expressions"][function]
                for idx in facts_dict:
                    facts.append(facts_dict[idx][1])
            pl_facts, facts_sat = check_satisfiability(facts)
            
            if not facts_sat:

                pdevs_facts = Facts_Generator_Agent.ask(f"- SYSTEM DESCRIPTION:\n\n{sys_des}\n\n-ATOMIC COMPONENET: {comp}\n\n- GENERATED FACTS:\n")
                print(json.dumps(pdevs_facts, indent=4))
                PL_statements = PL_conversion_pdevs(pdevs_facts, component = comp, props = props, engine='openai', model='gpt-4o-mini')
                print(json.dumps(PL_statements, indent=4, ensure_ascii=False))
                
            else:
                break

        modification_prompt = 'Verify whether the following behavioral conditions are already entailed by the generated facts. Analyze properly and only modify if needed to suffice the system description. Maintain Logical Consistency by avoiding contradictions.\n\n'

        ## Segregated Entailment Verification
        for function in lookup_dict:
            if en_check_dict[function] == True:
                continue
            print(f"Entailment check for {function}")
            facts_dict = PL_statements["Logical Expressions"][function]
            facts = []
            for idx in facts_dict:
                facts.append(facts_dict[idx][1])
            print('facts: ', facts)
            pl_facts, sat = check_satisfiability(facts)

            conds_dict = bc_PL_statements[lookup_dict[function]]
            conds = []
            for idx in conds_dict:
                conds.append(conds_dict[idx][1])
            print('conditions: ', conds)
            pl_conds, sat = check_satisfiability(conds)
            unentail_conds = check_entailment(pl_facts, pl_conds)
            unentail_conds_cnt += len(unentail_conds)

            if len(unentail_conds) > 0:
                en_check_dict[function] = False
                
                unentail_conds_str = []
                for cond_idx in unentail_conds:
                    unentail_conds_str.append(conds_dict[str(cond_idx)][0])
                modification_prompt += f"{function}:\n\n{'\n'.join(unentail_conds_str)}\n\n"
            else:
                en_check_dict[function] = True
        if unentail_conds_cnt < min_unentail_conds_cnt:
            print(f"entailment check - {en_chk_cnt} resulted in minumum unentailed conditions")
            min_unentail_conds_cnt = unentail_conds_cnt
            fin_pdevs_facts = pdevs_facts

        if en_check_dict["internal transition function"] and en_check_dict["external transition function"] and en_check_dict["output function"]:
            break

        modification_prompt += "Include any missing ports, phases and state variables according, fix errors, and ensure time advance is present for transitions. Strictly, retain the needed states and transitions. Return the full updated facts in the json format only. No additional text needed outside json."
        
        if en_chk_cnt < 2:
            pdevs_facts = Facts_Generator_Agent.ask(modification_prompt)
            PL_statements = PL_conversion_pdevs(pdevs_facts, component = comp, props = props, engine='openai', model='gpt-4o-mini')

    return fin_pdevs_facts