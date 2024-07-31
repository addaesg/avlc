import customtkinter
from CTkTable import *
from simplex import Tableau
from app import SimplexApp

def main(): 
    t = Tableau([-2,-3,-2])
    t.add_constraint([2, 1, 1], 4)
    t.add_constraint([1, 2, 1], 7)
    t.add_constraint([0, 0, 1], 5)

    simplexApp = SimplexApp(tabluex=t)
    simplexApp.mainloop()

if __name__ == "__main__":
    main()