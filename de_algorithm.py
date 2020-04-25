from random import random, randint

from py_expression_eval import Parser
from math import *
import numpy as np


def initialization(formula_variables, bounds, population):  # losuje populacje wektorów
    x = []  # cala populacja wektorow
    for i in range(0, population):  # for zeby zliczac wektory
        x_temp = []  # pojedyczy wektor
        for key in formula_variables:  # tyle ile kluczy tyle zmiennych wiec git
            x_temp.append(random() * (bounds.get(key)[1] - bounds.get(key)[0]) + bounds.get(key)[0])  # po kluczach
            #  losuje kolejne elementy wektorów zeby ogarnac jakie maja ograniczenia
        x.append(x_temp)  # dodaje ten wektor do calej populacji
    return x


def check_bounds(vector, formula_variables, bounds):
    temp = 0
    for i in range(0, len(vector)):  # for zeby zliczac wektory
        for key in formula_variables:
            lower_bound = bounds.get(key)[0]
            higher_bound = bounds.get(key)[1]
            if vector[i][temp] < lower_bound:
                vector[i][temp] = lower_bound
            if vector[i][temp] > higher_bound:
                vector[i][temp] = higher_bound
            temp = temp + 1
        temp = 0
    return vector


def mutation(x, formula_variables, bounds, F):
    v = [None] * len(x)  # tablica do u
    rand4 = [None] * 4  # tablica losowanych indeksow
    for nr_wektora in range(0, len(x)):  # dla kazdego wektora
        rand4[0] = nr_wektora  # 1 indeks to indeks wektora ktory bedziemy przeksztalcac
        for i in range(1, 4):
            rand4[i] = randint(0, len(x) - 1)
            for j in range(0, i):
                if rand4[j] == rand4[i]:
                    rand4[i] = randint(0, len(x) - 1)
                    j = -1
        v[nr_wektora] = np.add(x[rand4[1]], F * (np.subtract(x[rand4[2]], x[rand4[3]]))).tolist()
    v = check_bounds(v, formula_variables, bounds)
    return v


def crossover(x, v, CR):
    u = [None] * len(x)
    for i in range(0, len(x)):
        rand_U = random()
        if rand_U <= CR or i < randint(i, len(x) - 1):
            u[i] = v[i]
        else:
            u[i] = x[i]
    return u


def selection(x, u, function, formula_variables):
    for i in range(0, len(x)):
        f_x = function.evaluate(dict(zip(formula_variables, x[i])))
        f_u = function.evaluate(dict(zip(formula_variables, u[i])))
        if f_u <= f_x:
            x[i] = u[i]
    return x


def best_choice(x, function, formula_variables):
    min_f = function.evaluate(dict(zip(formula_variables, x[0])))
    best_x = x[0]
    for i in range(1, len(x)):
        if function.evaluate(dict(zip(formula_variables, x[i]))) < min_f:
            min_f = function.evaluate(dict(zip(formula_variables, x[i])))
            best_x = x[i]
    return best_x


def de_algorithm(function, formula_variables, bounds, iterations, population, F, CR):
    variables_name = ['x1', 'x2', 'x3', 'x4', 'x5']
    variables_bounds = dict(zip(variables_name, bounds))
    x = initialization(formula_variables, variables_bounds, population)
    for i in range(0, iterations):
        v = mutation(x, formula_variables, variables_bounds, F)
        u = crossover(x, v, CR)
        x = selection(x, u, function, formula_variables)

    best_x = best_choice(x, function, formula_variables)

    return best_x  # nieposortowane wartosci
