from typing import List

def parse_clause(line: str) -> frozenset:
    literals = list(map(int, line.strip().split()))
    return frozenset(lit for lit in literals if lit != 0)

def eliminate_var(var, clauses):
    new_clauses = []
    for clause in clauses:
        if var in clause:
            continue
        if -var in clause:
            new_clause = clause - {-var}
            if not new_clause:
                return None
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def dp_algorithm(clauses):
    variables = set(abs(lit) for clause in clauses for lit in clause)
    while variables:
        var = variables.pop()
        clauses_pos = eliminate_var(var, clauses)
        if clauses_pos is None:
            return "Formula este NESATISFIABILA (contradicție prin eliminare pozitivă)."
        clauses_neg = eliminate_var(-var, clauses)
        if clauses_neg is None:
            return "Formula este NESATISFIABILA (contradicție prin eliminare negativă)."
        clauses = list({frozenset(c) for c in clauses_pos + clauses_neg})
    return "Formula este SATISFIABILA (nu s-a generat contradicție)."

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

    result = dp_algorithm(clauses)
    print("\nRezultat:")
    print(result)

if __name__ == "__main__":
    main()
