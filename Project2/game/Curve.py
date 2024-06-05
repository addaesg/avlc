import pygame
from game.Point import Point, ControlPoints
import game.Color as Color
import numpy as np
import math


class InterpolatedCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True

    ## Lagrange Interpolation
    def calculate(self):
        self.samples = []
        n = len(self.controlPoints) - 1
        for t in np.arange(0, n, 0.005):
            sample = np.zeros(2, float)
            for i in range(n+1):
                control = self.controlPoints[i]
                control = np.array([control.x, control.y])
                p = [1, 1]
                for j in range(n+1):
                    if i != j:
                        p[0] *= t - j
                        p[1] *= i - j
                idk = p[0]/p[1]
                sample += np.dot(control, idk)
            sample = sample.astype(int)
            self.samples.append(Point(sample[0], sample[1], self.thickness, self.color))

    def draw(self, screen):
        self.calculate()
        for point in self.samples:
            point.draw(screen)

class MonomialInterpolatedCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.dated = True

    def back_sub(self, U, b):
        """x = back_sub(U, b) is the solution to U x = b
        U must be an upper-triangular matrix
        b must be a vector of the same leading dimension as U
        """
        n = U.shape[0]
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            tmp = b[i]
            for j in range(i+1, n):
                tmp -= U[i,j] * x[j]
            x[i] = tmp / U[i,i]
        return x

    def forward_sub(self, L, b):
        """x = forward_sub(L, b) is the solution to L x = b
        L must be a lower-triangular matrix
        b must be a vector of the same leading dimension as L
        """
        n = L.shape[0]
        x = np.zeros(n)
        for i in range(n):
            tmp = b[i]
            for j in range(i-1):
                tmp -= L[i,j] * x[j]
            x[i] = tmp / L[i,i]
        return x

    def lu_solve(self, L, U, b):
        """x = lu_solve(L, U, b) is the solution to L U x = b
        L must be a lower-triangular matrix
        U must be an upper-triangular matrix of the same size as L
        b must be a vector of the same leading dimension as L
        """
        y = self.forward_sub(L, b)
        x = self.back_sub(U, y)
        return x

    def lup_solve(self, L, U, P, b):
        """x = lup_solve(L, U, P, b) is the solution to L U x = P b
        L must be a lower-triangular matrix
        U must be an upper-triangular matrix of the same shape as L
        P must be a permutation matrix of the same shape as L
        b must be a vector of the same leading dimension as L
        """
        z = np.dot(P, b)
        x = self.lu_solve(L, U, z)
        return x

    def lup_decomp(self, A):
        """(L, U, P) = lup_decomp(A) is the LUP decomposition P A = L U
        A is any matrix
        L will be a lower-triangular matrix with 1 on the diagonal, the same shape as A
        U will be an upper-triangular matrix, the same shape as A
        U will be a permutation matrix, the same shape as A
        """
        n = A.shape[0]
        if n == 1:
            L = np.array([[1]])
            U = A.copy()
            P = np.array([[1]])
            return (L, U, P)

        if A.size == 0:
            raise ValueError("Matrix A is empty")

        i = np.argmax(np.abs(A[:, 0]))
        A_bar = np.vstack([A[i, :], A[:i, :], A[(i + 1):, :]])

        A_bar11 = A_bar[0, 0]
        A_bar12 = A_bar[0, 1:]
        A_bar21 = A_bar[1:, 0]
        A_bar22 = A_bar[1:, 1:]

        if A_bar22.size == 0:
            S22 = A_bar22
            L22, U22, P22 = np.array([[]]), np.array([[]]), np.array([[]])
        else:
            S22 = A_bar22 - np.dot(A_bar21[:, np.newaxis], A_bar12[np.newaxis, :]) / A_bar11
            (L22, U22, P22) = self.lup_decomp(S22)

        L11 = np.array([[1]])
        U11 = np.array([[A_bar11]])

        L12 = np.zeros((1, n-1))
        U12 = A_bar12.reshape(1, -1)

        if A_bar21.size > 0:
            L21 = (np.dot(P22, A_bar21) / A_bar11).reshape(-1, 1)
        else:
            L21 = np.zeros((n-1, 1))
        U21 = np.zeros((n-1, 1))

        L = np.block([[L11, L12], [L21, L22]])
        U = np.block([[U11, U12], [U21, U22]])

        P_top = np.hstack([np.zeros((1, i)), np.ones((1, 1)), np.zeros((1, n-i-1))])
        P_bottom_left = P22[:, :(i)] if i > 0 else np.zeros((n-1, 0))
        P_bottom_right = P22[:, i:] if i < n-1 else np.zeros((n-1, 0))
        P_bottom = np.hstack([P_bottom_left, np.zeros((n-1, 1)), P_bottom_right])
        P = np.vstack([P_top, P_bottom])

        return (L, U, P)


    def linear_solve(self, A, b):
        """x = linear_solve(A, b) is the solution to A x = b (computed with partial pivoting)
        A is any matrix
        b is a vector of the same leading dimension as A
        x will be a vector of the same leading dimension as A
        """
        (L, U, P) = self.lup_decomp(A)
        x = self.lup_solve(L, U, P, b)
        return x

    ## Monomial Interpolation
    def calculate(self):
        numberOfPoints = len(self.controlPoints)
        exponents = np.arange(numberOfPoints)
        matrix = np.zeros((numberOfPoints, numberOfPoints))
        column_vector_Y = np.zeros(numberOfPoints)
        for idx, p in enumerate(self.controlPoints):
            matrix[idx, :] = np.power(p.x, exponents)
            column_vector_Y[idx] = p.y
        print(matrix)
        try:
            x = self.linear_solve(matrix, column_vector_Y)
            print(x)
        except:
            print("não deu")
            

    def draw(self, screen):
        self.calculate()
        for point in self.samples:
            point.draw(screen)

class BezierCurve:
    def __init__(self, controlPoints, color=Color.WHITE, width=10, samples=10000):
        self.controlPoints = controlPoints
        self.color = color
        self.thickness = width
        self.samples = []
        self.sampleCount = samples
        self.dated = True

    def calculate(self):
        self.samples = []
        n = len(self.controlPoints) - 1
        for t in np.arange(0, 1, 0.001):
            sample = np.zeros(2)
            for i in range(n + 1):
                control = self.controlPoints[i]
                control = np.array([control.x, control.y])
                idk = (math.factorial(n)/(math.factorial(i)*math.factorial(n-i))) *((1-t)**(n-i))*(t**i)
                sample += np.dot(idk, control)
            sample = sample.astype(int)
            self.samples.append(Point(sample[0], sample[1], self.thickness, self.color))

    def draw(self, screen):
        self.calculate()
        for point in self.samples:
            point.draw(screen)
        for i in range(1, len(self.controlPoints)):
            pygame.draw.line(screen, Color.BLUE, self.controlPoints[i-1].pos(), self.controlPoints[i].pos(), self.thickness)



