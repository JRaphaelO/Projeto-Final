from __future__ import print_function
from ortools.linear_solver import pywraplp


class Solver:
    def __init__(self, n, m, B, T, F, products, materials):
        self.n = n
        self.m = m
        self.B = B
        self.T = T
        self.F = F
        self.products = products
        self.materials = materials

        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.infinity = self.solver.infinity()
        self.variables = {}

    def init_variables(self):
        for i in range(1, self.n + 1):
            self.variables[f'p{i}'] = self.solver.IntVar(
                0.0, self.infinity, f'p{i}')

        for j in range(1, self.m + 1):
            self.variables[f'x{j}'] = self.solver.IntVar(
                0.0, self.infinity, f'x{j}'
            )

        for i in range(1, self.n + 1):
            self.variables[f'z{i}'] = self.solver.IntVar(
                0.0, 1.0, f'z{i}')

    def create_restriction(self):
        self.solver.Add(
            self.solver.Sum([self.variables[f'p{i}'] * self.products[i-1]['b']
                             for i in range(1, self.n + 1)])
            + self.solver.Sum([self.variables[f'z{i}']
                               for i in range(1, self.n + 1)]) * self.T <= self.B
        )

        for i in range(1, self.n + 1):
            self.solver.Add(
                self.variables[f'p{i}'] >= self.products[i - 1]['DMIN'] * self.variables[f'z{i}'])

        for i in range(1, self.n + 1):
            self.solver.Add(
                self.variables[f'p{i}'] <= self.products[i - 1]['DMAX'] * self.variables[f'z{i}'])

        for j in range(1, self.m + 1):
            self.solver.Add(self.solver.Sum([self.variables[f'p{i}'] * self.products[i - 1][f'm{j}'] for i in range(
                1, self.n + 1)]) <= (self.variables[f'x{j}'] * self.materials[j - 1]['lote']))

    def set_function_objective(self):
        self.solver.Maximize(
            self.solver.Sum([self.variables[f'p{i}']*self.products[i - 1]['R'] for i in range(1, self.n + 1)]) -
            (self.F + self.solver.Sum(
                [self.variables[f'x{j}'] * self.materials[j - 1]['coast'] for j in range(1, self.m + 1)]))
        )

    def print_solution(self):
        if self.solver.Solve() == pywraplp.Solver.OPTIMAL:
            print(f'Lucro = R$ {int(self.solver.Objective().Value())}')
            print('Produtos:')
            for i in range(1, self.n + 1):
                product = self.variables[f'p{i}']
                b = self.products[i - 1]['b']
                r = self.products[i - 1]['R']
                print(
                    f'\tForam produzidos {int(product.solution_value())} produtos {product}, utilizou {product.solution_value()*b} horas na linha de producao, com a receita de R$ {int(product.solution_value()*r)}.')

            print('\nMaterias-primas:')
            for j in range(1, self.m + 1):
                x = self.variables[f'x{j}'].solution_value()
                coast = self.materials[j - 1]['coast']
                print(
                    f'Foram comprados {x} lotes da materia-prima m{j}, com o custo de R$ {int(x * coast)}.')

            hours = sum(
                [self.variables[f'z{i}'].solution_value() for i in range(1, self.n + 1)])
            print(
                f'\nA quantidade de horas que foram utilizadas na troca de produtos foi de {hours * self.T} horas.')

        else:
            print('The problem does not have an optimal solution.')
