import sys
from typing import List


def parse_dimacs(file_path: str) -> List[List[int]]:
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('c') or line.startswith('p'):
                continue
            literals = list(map(int, line.split()))
            if literals[-1] == 0:
                literals = literals[:-1]
            clauses.append(literals)
    return clauses


def unit_propagate(unit: int, clauses: List[List[int]]) -> List[List[int]]:
    return [
        [l for l in clause if l != -unit]
        for clause in clauses if unit not in clause
    ]


def pure_literal_assign(literal: int, clauses: List[List[int]]) -> List[List[int]]:
    return [clause for clause in clauses if literal not in clause]


def choose_literal(clauses: List[List[int]]) -> int:
    return clauses[0][0]


class DPLLSolver:
    def __init__(self, clauses: List[List[int]]):
        self.clauses = clauses

    def solve(self) -> bool:
        return self._dpll(self.clauses)

    def _dpll(self, clauses: List[List[int]]) -> bool:
        while (unit_clause := next((c[0] for c in clauses if len(c) == 1), None)) is not None:
            clauses = unit_propagate(unit_clause, clauses)

        all_literals = {l for clause in clauses for l in clause}
        pure_literals = {l for l in all_literals if -l not in all_literals}
        for literal in pure_literals:
            clauses = pure_literal_assign(literal, clauses)

        if not clauses:
            return True
        if any(len(clause) == 0 for clause in clauses):
            return False

        literal = choose_literal(clauses)
        return self._dpll(unit_propagate(literal, clauses)) or self._dpll(unit_propagate(-literal, clauses))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    formula = parse_dimacs(sys.argv[1])
    result = DPLLSolver(formula).solve()
    print("SATISFIABIL" if result else "NESATISFIABIL")
