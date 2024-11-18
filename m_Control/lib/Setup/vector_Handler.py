class VectorHandler:
    def __init__(self):
        self.current_vector = [0] * 6
        self.previous_vector = [0] * 6

    def vector_minimizer(self, vector):
        pairs = [(1, 0), (3, 2), (5, 4), (7, 6)]
        for idx, (i, j) in enumerate(pairs):
            self.current_vector[idx] = vector[i] - vector[j]
        self.current_vector[4] = vector[8]
        self.current_vector[5] = vector[9]

    def update_vector(self, vector):
        self.vector_minimizer(vector)
        if self.current_vector != self.previous_vector:
            self.previous_vector = self.current_vector.copy()
            print(self.current_vector)