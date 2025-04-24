from typing import List, Dict, Optional

def parse_clause(line: str) -> frozenset:
    literals = list(map(int, line.strip().split()))
    return frozenset(lit for lit in literals if lit != 0)

def dpll_algorithm(clauses: List[frozenset], assignment: Optional[Dict[int, bool]] = None) -> bool:
    if assignment is None:
        assignment = {}

    def is_clause_true(clause):
        return any((lit > 0 and assignment.get(abs(lit)) is True) or
                   (lit < 0 and assignment.get(abs(lit)) is False)
                   for lit in clause)

    def is_clause_false(clause):
        return all((lit > 0 and assignment.get(abs(lit)) is False) or
                   (lit < 0 and assignment.get(abs(lit)) is True)
                   for lit in clause if abs(lit) in assignment)

    clauses = [c for c in clauses if not is_clause_true(c)]
    if any(is_clause_false(c) for c in clauses):
        return False
    if not clauses:
        return True

    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        lit = next(iter(unit_clauses[0]))
        assignment[abs(lit)] = lit > 0
        return dpll_algorithm(clauses, assignment)

    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                for value in [True, False]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = value
                    if dpll_algorithm(clauses, new_assignment):
                        return True
                return False
    return True

def main():
    print("Introdu clauze în formatul: 1 -2 0 (0 marchează sfârșitul clauzei).")
    print("Apasă ENTER fără nimic pentru a termina introducerea.\n")

    clauses = []
    while True:
        line = input("Clauză: ").strip()
        if not line:
            break
        clause = parse_clause(line)
        if clause:
            clauses.append(clause)

    satisfiable = dpll_algorithm(clauses)
    print("\nRezultat:")
    if satisfiable:
        print("Formula este SATISFIABILA.")
    else:
        print("Formula este NESATISFIABILA.")

if __name__ == "__main__":
    main()
