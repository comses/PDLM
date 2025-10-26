import re
from z3 import *
import json

def replace_ops(s):
    """
    Replace logical operator symbols with parseable Z3/Python function names.
    Supports both unicode and ascii syntax.
    """
    s = s.replace('¬', 'Not ')
    s = s.replace('~', 'Not ')
    s = s.replace('∧', ' And ')
    s = s.replace('&', ' And ')
    s = s.replace('∨', ' Or ')
    s = s.replace('|', ' Or ')
    s = s.replace('→', ' Implies ')
    s = s.replace('=>', ' Implies ')
    # Add spaces to make tokenizing easier for multi-character variables
    return s

def parse_var_expr(expr, var_map):
    """
    Recursively parse a logic expression string into Z3 expressions.
    Assumes operators are replaced by Not/And/Or/Implies keywords.
    """
    expr = expr.strip()
    # Remove all redundant outer parentheses
    while expr.startswith('(') and expr.endswith(')'):
        # Check parentheses balance inside
        count, maxcount = 0, 0
        for c in expr[1:-1]:
            if c == '(': count += 1
            elif c == ')': count -= 1
            maxcount = max(maxcount, abs(count))
        if count != 0 or maxcount == 0: break
        expr = expr[1:-1].strip()
    # Handle Not
    if expr.startswith('Not'):
        after_not = expr[3:].strip()
        # Remove leading parentheses
        while after_not.startswith('(') and after_not.endswith(')'):
            after_not = after_not[1:-1].strip()
        return Not(parse_var_expr(after_not, var_map))
    # Handle Implies (lowest precedence), left-to-right
    # This supports only one Implies per level, which is fine for most natural uses
    if 'Implies' in expr:
        parts = expr.split('Implies', 1)
        left_part = parts[0].replace('(','').replace(')','').strip()
        right_part = parts[1].replace('(','').replace(')','').strip()
        return Implies(parse_var_expr(left_part, var_map), parse_var_expr(right_part, var_map))
    # Handle And, Or
    for op, fun in [('And', And), ('Or', Or)]:
        # Split on top-level operator (not inside parens)
        items = []
        depth = 0
        last = 0
        found = False
        expr_padded = expr + ' '  # to avoid last-token issues
        for i in range(len(expr_padded)):
            c = expr_padded[i]
            if c == '(': depth += 1
            elif c == ')': depth -= 1
            elif depth == 0 and expr_padded[i:i+len(op)] == op:
                items.append(expr_padded[last:i].strip())
                last = i+len(op)
                found = True
        if found:
            items.append(expr_padded[last:-1].strip())
            return fun(*(parse_var_expr(item, var_map) for item in items))
    # Leaf: variable
    expr = expr.strip()
    # while expr.startswith('(') and expr.endswith(')'):
    #     expr = expr[1:-1].strip()
    expr.replace('(', "").replace(')',"")
    if expr in var_map:
        return var_map[expr]
    raise KeyError(f"Unexpected variable/expression: '{expr}'")

def parse_rule(expr, var_map):
    expr = replace_ops(expr)
    return parse_var_expr(expr, var_map)

def check_satisfiability(stmts):
    # rule_strings = stmts.strip().split('\n')
    # Use regex to find identifiers (multi-char)
    var_pattern = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")
    all_vars = set()
    for rule in stmts:
        # if ':' in rule:
            # _, expr = rule.split(':', 1)
        for m in var_pattern.findall(rule):
            all_vars.add(m)
    var_map = {var: Bool(var) for var in all_vars}
    rules = []
    for rule_string in stmts:
        rule_string = rule_string.replace('(', '').replace(')', '').strip()
        # _, expr = rule_string.split(':', 1)
        rules.append(parse_rule(rule_string, var_map))
    s = Solver()
    labels = []
    label_to_rule = {}
    for i, rule in enumerate(rules):
        label = Bool(f'assump_{i}')
        s.add(Or(Not(label), rule))
        labels.append(label)
        label_to_rule[label] = rule
    result = s.check(labels)
    # print(result != unsat)
    return rules, result != unsat

def check_entailment(facts, conditions):
    unentailed_rules = []
    for idx, cond in enumerate(conditions, 1):
        solver = Solver()
        solver.add(facts)
        solver.add(Not(cond))  # Entailment test: facts ⊨ cond ⇔ facts ∧ ¬cond is UNSAT

        result = solver.check()
        if result == unsat:
            print(f"✅ Condition C{idx} IS entailed by the facts.")
        elif result == sat:
            print(f"❌ Condition C{idx} is NOT entailed by the facts.")
            unentailed_rules.append(idx)
    return unentailed_rules