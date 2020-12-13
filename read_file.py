class ReadFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = None

    def load_file(self):
        self.data = open(f'./input/{self.filename}', 'r')

    def split_file(self):
        lines = self.data.readlines()
        n = int(lines[0])
        m = int(lines[1])
        B = int(lines[2])
        T = int(lines[3])
        F = int(lines[4])

        products = []

        for i in range(5, 5 + n):
            p = lines[i].split(' ')
            product = {}

            for j in range(1, m + 1):
                product[f'm{j}'] = int(p[j - 1])

            product['b'] = float(p[m])
            product['DMIN'] = int(p[m + 1])
            product['DMAX'] = int(p[m + 2])
            product['R'] = int(p[m + 3])
            products.append(product)

        materials = []
        for i in range(5 + n, 5 + n + m):
            material = {}
            l = lines[i].split()
            material['lote'] = int(l[0])
            material['coast'] = int(l[1])
            materials.append(material)

        return n, m, B, T, F, products, materials
