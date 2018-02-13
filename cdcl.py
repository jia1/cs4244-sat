import sys

input_cnf_file = 'input.cnf.sample'

def is_positive(variable):
    return variable > 0

def is_negative(variable):
    return not is_positive(variable)

def negate_assignment(assignment):
    return assignment ^ 1

def negate_variable(variable):
    return -1 * variable

def get_assignment(variable, assignments):
    if abs(variable) not in assignments:
        return None
    assignment = assignments[variable]
    return assignment if is_positive(variable) else negate_assignment(assignment)

def get_sorted_clauses(clauses):
    return sorted(clauses, key=len)

def or_sat(clauses, assignments):
    has_unassigned_variables = False
    for variable in clause:
        assignment = get_assignment(variable, assignments)
        if assignment is None:
            has_unassigned_variables = True
            continue
        if assignment:
            return True
    return None if has_unassigned_variables else False

def unit_propagation(clauses, assignments):
    has_conflict, clauses = propagate(clauses, assignments)
    if has_conflict:
        return (False, clauses, assignments)
    clauses = get_sorted_clauses(clauses)
    i = 0
    while i < len(clauses):
        clause = clauses[i]
        if len(clause) == 1:
            variable = clause[0]
            if is_positive(variable):
                assignments[variable] = 1
            else:
                assignments[negate_variable(variable)] = 0
            variable = abs(variable)
            has_conflict, clauses = propagate(clauses, {variable: assignments[variable]})
            if has_conflict:
                return (False, clauses, assignments)
    return (True, clauses, assignments)

def propagate(clauses, assignments):
    for (variable, assignment) in assignments.items():
        i = 0
        while i < len(clauses):
            clause = clauses[i]
            if (variable in clause and assignment or
                negate_variable(variable) in clause and negate_assignment(assignment)):
                clauses.pop(i)
            else:
                clauses[i].discard(variable)
                clauses[i].discard(negate_variable(variable))
                if not clauses[i]:
                    return (False, clauses)
    return (True, clauses)

def all_variables_assigned(clauses, assignments):
    variables = set()
    for clause in clauses:
        variables.update(map(lambda variable: abs(variable), clause))
    return len(assignments) == len(variables)

def pick_branching_variable(clauses, assignments):
    pass

def conflict_analysis(clauses, assignments):
    pass

def backtrack(clauses, assignments, beta):
    pass

def cdcl(clauses, assignments):
    if not unit_propagation(clauses, assignments):
        return (False, assignments)
    decision_level = 0
    while not all_variables_assigned(clauses, assignments):
        (variable, assignment) = pick_branching_variable(clauses, assignments)
        decision_level += 1
        assignments[variable] = assignment
        if not unit_propagation(clauses, assignments):
            beta = conflict_analysis(clauses, assignments)
            if beta < 0:
                return (False, assignments)
            else:
                backtrack(clauses, assignments, beta)
                decision_level = beta
    return (True, assignments)

def solve(clauses):
    is_sat, assignments = cdcl(clauses, {})
    if is_sat:
        return ('SAT', assignments)
    else:
        return ('UNSAT', assignments)

with open(input_cnf_file) as f:
    lines = filter(
        lambda line: line[0] != 'c',
        map(
            lambda line: line.strip().split(' '),
            f.readlines()))
    number_of_variables, number_of_clauses = map(
        int,
        next((line[2:4] for line in lines if line[:2] == ['p', 'cnf']), [-1, -1]))
    if number_of_variables < 0 or number_of_clauses < 0:
        print('Invalid .cnf file: No p cnf declaration')
        sys.exit()
    clauses = map(
        lambda line: set(map(int, line[:-1])),
        filter(
            lambda line: line[:2] != ['p', 'cnf'] and line[-1] == '0',
            lines))
    clauses = get_sorted_clauses(clauses)
    if len(clauses) != number_of_clauses:
        print('Invalid .cnf file: Number of clauses found contradicts p cnf declaration')
        sys.exit()
    variables = set()
    for clause in clauses:
        variables.update(map(lambda variable: abs(variable), clause))
    if len(variables) != number_of_variables:
        print('Invalid .cnf file: Number of variables found contradicts p cnf declaration')
        sys.exit()
    print(solve(clauses))
