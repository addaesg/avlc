import pygame
import game.Color as Color
import numpy as np


def lup_decomp(A):
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
        (L22, U22, P22) = lup_decomp(S22)

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


def fwd_sub(L, c):
    result = np.zeros_like(c, dtype=np.double)
    for i in range(len(c)):
        result[i] = c[i] - np.dot(L[i, :i],  result[:i])
    return result 

def bwd_sub(U, c):
    result = np.zeros_like(c, dtype=np.double)
    for i in range(len(c)-1, -1, -1):
        result[i] = (c[i] - np.dot(U[i, i+1:], result[i+1:])) / U[i, i]
    return result

def linear_solve(A, b):
    (L, U, P) = lup_decomp(A)
    return bwd_sub(U, fwd_sub(L, np.dot(P, b)))