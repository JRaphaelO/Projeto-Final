from read_file import ReadFile
from solver import Solver


def main(filename: str):
    read_file = ReadFile(filename)
    read_file.load_file()
    n, m, B, T, F, products, materials = read_file.split_file()

    solver = Solver(n, m, B, T, F, products, materials)
    solver.init_variables()
    solver.create_restriction()
    solver.set_function_objective()
    solver.print_solution()


if __name__ == '__main__':
    file = 'data.txt'
    main(file)
