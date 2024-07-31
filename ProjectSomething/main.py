import customtkinter
from CTkTable import *
from simplex import Tableau
from app import SimplexApp


def main():
    # Função objetivo com coeficientes reajustados (coletando coeficientes com sinais invertidos)
    t = Tableau([-80, -120, -100, -70, -110, -90, -75, -115, -95, -130])

    # Restrições de capacidade dos telescópios (permanece o mesmo)
    t.add_constraint([1, 1, 1, 0, 0, 0, 0, 0, 0, 0], 10)
    t.add_constraint([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 15)
    t.add_constraint([0, 0, 0, 0, 0, 0, 1, 1, 1, 1], 20)

    # Restrição de custo (permanece o mesmo)
    t.add_constraint([500, 700, 600, 450, 650, 550, 400, 600, 500, 700], 50000)

    # Restrições de tempo mínimo de observação (permanece o mesmo)
    t.add_constraint([-1, 0, 0, -1, 0, 0, -1, 0, 0, 0], -2)
    t.add_constraint([0, -1, 0, 0, -1, 0, 0, -1, 0, 0], -3)
    t.add_constraint([0, 0, -1, 0, 0, -1, 0, 0, -1, 0], -2)
    t.add_constraint([0, 0, 0, 0, 0, 0, 0, 0, 0, -1], -1)

    simplexApp = SimplexApp(tabluex=t)
    simplexApp.mainloop()


if __name__ == "__main__":
    main()
