# Davis-Putnam SAT Solver în Python (format DIMACS)

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


def unit_propagation(clauses):
    assignment = set()
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = next(iter(unit_clauses[0]))
        assignment.add(unit)
        clauses = [c for c in clauses if unit not in c]
        clauses = [c - {-unit} for c in clauses]
        if any(len(c) == 0 for c in clauses):
            return clauses, assignment, False
        unit_clauses = [c for c in clauses if len(c) == 1]
    return clauses, assignment, True


def pure_literal_elimination(clauses):
    assignment = set()
    literals = {lit for clause in clauses for lit in clause}
    pure_literals = set()
    for l in literals:
        if -l not in literals:
            pure_literals.add(l)
    while pure_literals:
        lit = pure_literals.pop()
        assignment.add(lit)
        clauses = [c for c in clauses if lit not in c]
        literals = {lit for clause in clauses for lit in clause}
        pure_literals = {l for l in literals if -l not in literals}
    return clauses, assignment


def davis_putnam(clauses):
    clauses, unit_assignment, success = unit_propagation(clauses)
    if not success:
        return False

    clauses, pure_assignment = pure_literal_elimination(clauses)

    if not clauses:
        return True
    if any(len(c) == 0 for c in clauses):
        return False

    l = next(iter(next(iter(clauses))))

    new_clauses = clauses + [{l}]
    if davis_putnam(new_clauses):
        return True

    new_clauses = clauses + [{-l}]
    return davis_putnam(new_clauses)


# Exemplu utilizare
if __name__ == "__main__":
    print("Introduceți formula în format DIMACS (finalizați input-ul cu o linie goală):")
    dimacs_input = ""
    while True:
        line = input()
        if line.strip() == "":
            break
        dimacs_input += line + "\n"

    clauses = parse_dimacs(dimacs_input)
    result = davis_putnam(clauses)

    if result:
        print("Formula este SATISFIABILĂ")
    else:
        print("Formula NU este satisfiabilă")
