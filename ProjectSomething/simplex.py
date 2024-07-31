from numpy import *


class Tableau:
    def __init__(self, obj):
        self.obj = [1] + obj
        self.rows = []
        self.cons = []
        self.num_variables = len(obj)
        self.num_constraints = 0

        ## bloat for gui's sake
        self.cur_step = 0
        self.n_steps = 0
        self.livre = ""
        self.constrained = ""
        self.initial_obj = [1] + obj
        self.initial_constraints = []

    def add_constraint(self, expression, value, isReset=False):
        self.rows.append([0] + expression)
        self.cons.append(value)
        self.num_constraints += 1
        self.header_tableau = (
            ["Basic"]
            + ["x" + str(i + 1) for i in range(self.num_variables)]
            + ["s" + str(i + 1) for i in range(self.num_constraints)]
            + ["Solution"]
        )

        self.basic_variables = ["s" + str(i + 1) for i in range(self.num_constraints)]

        if not isReset:
            self.initial_constraints.append([expression, value])

    def build_tableau(self):
        # build full tableau
        for i in range(len(self.rows)):
            self.obj += [0]
            ident = [0 for r in range(len(self.rows))]
            ident[i] = 1
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=float)
        self.obj = array(self.obj + [0], dtype=float)

    def next_step(self):
        if self._check():
            return
        c = self._pivot_column()
        r = self._pivot_row(c)
        self._pivot(r, c)
        self.livre = self.header_tableau[c]
        self.constrained = self.basic_variables[r]
        for index, item in enumerate(self.basic_variables):
            if self.basic_variables[index] == self.basic_variables[r]:
                self.basic_variables[index] = self.header_tableau[c]
        self.cur_step += 1

    def reset(self):
        self.obj = [1] + self.initial_obj[1:]
        self.rows = []
        self.cons = []
        self.num_variables = len(self.obj) - 1
        self.num_constraints = 0
        self.livre = ""
        self.constrained = ""
        self.cur_step = 0
        for i in range(len(self.initial_constraints)):
            self.add_constraint(
                self.initial_constraints[i][0],
                self.initial_constraints[i][1],
                isReset=True,
            )
        self.build_tableau()

    def _pivot_column(self):
        low = 0
        idx = 0
        for i in range(1, len(self.obj) - 1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == 0:
            return -1
        return idx

    def _pivot_row(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        ratio = []
        for i in range(len(rhs)):
            if lhs[i] == 0:
                ratio.append(float("inf"))
                continue
            value = rhs[i] / lhs[i]
            if value < 0.0:
                ratio.append(float("inf"))
                continue
            ratio.append(value)
        return argmin(ratio)

    def _pivot(self, row, col):
        e = self.rows[row][col]
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row:
                continue
            self.rows[r] = self.rows[r] - self.rows[r][col] * self.rows[row]
        self.obj = self.obj - self.obj[col] * self.rows[row]

    def _check(self):
        if min(self.obj[1:-1]) >= 0:
            return True
        return False

    def setup(self):
        ## bloated code
        ## we need the number of step to calculate the progress bar
        self.n_steps = 0
        self.build_tableau()
        while not self._check():
            self.next_step()
            self.n_steps += 1
        self.reset()
