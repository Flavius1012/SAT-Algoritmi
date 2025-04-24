def parse_dimacs(dimacs_str):
    clauses = []
    for line in dimacs_str.splitlines():
        line = line.strip()
        if line.startswith('c') or line.startswith('p') or not line:
            continue
        literals = list(map(int, line.split()))
        clause = set(literals[:-1])  # elimină 0-ul de la final
        clauses.append(clause)
    return clauses


def unit_propagate(clauses):
    assignment = set()
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = next(iter(unit_clauses[0]))
        assignment.add(unit)
        clauses = [c for c in clauses if unit not in c]
        clauses = [c - {-unit} for c in clauses]
        if any(len(c) == 0 for c in clauses):
            return clauses, False
        unit_clauses = [c for c in clauses if len(c) == 1]
    return clauses, True


def pure_literal_assign(clauses):
    literals = {lit for clause in clauses for lit in clause}
    assignment = set()
    pure_literals = {l for l in literals if -l not in literals}
    while pure_literals:
        lit = pure_literals.pop()
        assignment.add(lit)
        clauses = [c for c in clauses if lit not in c]
        literals = {lit for clause in clauses for lit in clause}
        pure_literals = {l for l in literals if -l not in literals}
    return clauses


def choose_literal(clauses):
    for clause in clauses:
        for lit in clause:
            return lit


def dpll(clauses):
    clauses, success = unit_propagate(clauses)
    if not success:
        return False

    clauses = pure_literal_assign(clauses)

    if not clauses:
        return True
    if any(len(c) == 0 for c in clauses):
        return False

    l = choose_literal(clauses)
    return dpll(clauses + [{l}]) or dpll(clauses + [{-l}])

if __name__ == "__main__":
    print("Introduceți formula în format DIMACS (finalizați input-ul cu o linie goală):")
    dimacs_input = ""
    while True:
        line = input()
        if line.strip() == "":
            break
        dimacs_input += line + "\n"

    clauses = parse_dimacs(dimacs_input)
    result = dpll(clauses)

    if result:
        print("Formula este SATISFIABILĂ")
    else:
        print("Formula NU este satisfiabilă")
