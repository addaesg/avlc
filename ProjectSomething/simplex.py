from numpy import *


class Tableau:
  def __init__(self, obj):
    self.obj = [1] + obj
    self.rows = []
    self.cons = []
    self.num_variables = len(obj)
    self.num_constraints = 0

  def add_constraint(self, expression, value):
    self.rows.append([0] + expression)
    self.cons.append(value)
    self.num_constraints += 1
    self.header_tableau = ["Basic"] + ["x"+str(i+1) for i in range(self.num_variables)] \
                                    + ["s"+str(i+1) for i in range(self.num_constraints)] \
                                    + ["Solution"]
            
    self.basic_variables = ["s"+str(i+1) for i in range(self.num_constraints)]

  def _pivot_column(self):
    low = 0
    idx = 0
    for i in range(1, len(self.obj)-1):
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
        ratio.append(float('inf'))
        continue
      ratio.append(rhs[i]/lhs[i])
    return argmin(ratio)

  def display(self):   
    # Formatting the output in float with 2 decimal places
    fmt = '{:<8}'.format("Basic") \
        + "".join(['{:>8}'.format("x"+str(i+1)) for i in range(self.num_variables)])   \
        + "".join(['{:>8}'.format("s"+str(i+1)) for i in range(self.num_constraints)]) \
        + '{:>8}'.format("Sol.")

    fmt += "\n" 
    fmt += '{:<8}'.format("z") + "".join(["{:>8.2f}".format(item) for item in self.obj[1:]])

    for i, row in enumerate(self.rows):
      fmt += "\n" 
      fmt += '{:<8}'.format(self.basic_variables[i]) \
            + "".join(["{:>8.2f}".format(item) for item in row[1:]])
    print(fmt)

  def _pivot(self, row, col):
    e = self.rows[row][col]
    self.rows[row] /= e
    for r in range(len(self.rows)):
      if r == row: 
        continue
      self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
    self.obj = self.obj - self.obj[col]*self.rows[row]

  def _check(self):
    if min(self.obj[1:-1]) >= 0: 
      return True
    return False
        
  def solve(self):
    # build full tableau
    for i in range(len(self.rows)):
      self.obj += [0]
      ident = [0 for r in range(len(self.rows))]
      ident[i] = 1
      self.rows[i] += ident + [self.cons[i]]
      self.rows[i] = array(self.rows[i], dtype=float)
    self.obj = array(self.obj + [0], dtype=float)

    # solve
    self.display()
    while not self._check():
      c = self._pivot_column()
      r = self._pivot_row(c)
      self._pivot(r,c)
      print('\n')
      print('Entering Variable: ', self.header_tableau[c])
      print('Leaving Variable : ', self.basic_variables[r])
      print('\n')
      # Updating the basic variable
      for index, item in enumerate(self.basic_variables):
        if self.basic_variables[index] == self.basic_variables[r]:
          self.basic_variables[index] = self.header_tableau[c]
      self.display()
            
if __name__ == '__main__':

  """
  max 
    2x + 1y  = z 
  st
    2x + 3y <= 3
     x + 5y <= 1
    2x +  y <= 4
    4x +  y <= 5
     x ,  y >= 0
  """
  """
  MAX Z = 80x_1 + 120x_2 + 100x_3 + 70x_4 + 110x_5 + 90x_6 + 75x_7 + 115x_8 + 95x_9 + 130x_10
  subject to
  x_1 + x_2 + x_3 <= 10,
  x_4 + x_5 + x_6 <= 15,
  x_8 + x_9 + x_10 <= 20,
  500x_1 + 700x_2 + 600x_3 + 450x_4 + 650x_5 + 550x_6 + 400x_7 + 600x_8 + 500x_9 + 700x_10 <= 50000,
  -x_1 - x_4 - x_7 <= -2,
  -x_2 - x_5 - x_8 <= -3,
  -x_3 - x_6 - x_9 <= -2,
  -x_10 <= -1
  and x_1 >= 0,x_2 >= 0,x_3 >= 0,x_4 >= 0,x_5 >= 0,x_6 >= 0,x_7 >= 0,x_8 >= 0,x_9 >= 0,x_10 >= 0 
  """

  # t = Tableau([-2,-1])
  # t.add_constraint([2, 3], 3)
  # t.add_constraint([1, 5], 1)
  # t.add_constraint([2, 1], 4)
  # t.add_constraint([4, 1], 5)
  t = Tableau([-80, -120, -100, -70, -110, -90, -75, -115, -95, -130])
  t.add_constraint([1, 1, 1, 0, 0, 0, 0, 0, 0, 0], 10)
  t.add_constraint([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 15)
  t.add_constraint([0, 0, 0, 0, 0, 0, 1, 1, 1, 1], 20)
  t.add_constraint([500, 700, 600, 450, 650, 550, 400, 600, 500, 700], 50000)
  t.add_constraint([-1, 0, 0, -1, 0, 0, -1, 0, 0, 0], -2)
  t.add_constraint([0, -1, 0, 0, -1, 0, 0, -1, 0, 0], -3)
  t.add_constraint([0, 0, -1, 0, 0, -1, 0, 0, -1, 0], -2)
  t.add_constraint([0, 0, 0, 0, 0, 0, 0, 0, 0, -1], -1)
  t.solve()