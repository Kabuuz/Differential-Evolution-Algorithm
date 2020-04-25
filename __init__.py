from tkinter import *
from tkinter import messagebox
from py_expression_eval import Parser
import re
from math import *
from random import random, randint
import numpy as np
from de_algorithm import de_algorithm

max_number_of_variables = 5
sample_function = 'x1^4+x2^4-0.62*x1^2-0.62*x2^2'
rosenbrock_function = '100*(x2-x1^2)^2+(1-x1)^2'
zangwill_function = '(x1-x2+x3)^2+(-x1+x2+x3)^2+(x1+x2-x3)^2'
goldstein_price_function = '(1+(x1+x2+1)^2*(19-14*x1+3*x1^2-14*x2+6*x1*x2+3*x2^2))*(30+(2*x1-3*x2)^2*(18-32*x1+12*x1^2+48*x2-36*x1*x2+27*x2^2))'
rastrigin_function = '(x1^2-cos(18*x1))+(x2^2-cos(18*x2))+(x3^2-cos(18*x3))'


def enter_function(entry, function):
    entry.delete(0, END)
    entry.insert(0, function)


def init_window():
    width = 480
    height = 370

    title = "Algorytm Ewolucji Różnicowej"

    global window
    window = Tk()

    window.title(title)
    window.geometry(str(width) + "x" + str(height))
    window.resizable(width=False, height=False)

    label_space1 = Label(window, text='', width=5)
    label_space1_row = 0
    label_space1.grid(column=0, row=label_space1_row)

    label_formula = Label(window, text="f(x):", width=5)
    label_formula_row = label_space1_row + 1
    label_formula.grid(column=0, row=label_formula_row)
    label_formula.config(anchor=E)

    entry_formula = Entry(window, width=70)
    entry_formula_row = label_formula_row
    entry_formula.grid(column=1, columnspan=14, row=entry_formula_row)

    label_space2 = Label(window, text='', width=5)
    label_space2_row = entry_formula_row + 1
    label_space2.grid(column=0, row=label_space2_row)

    label_parameters = Label(window, text="Parametry:", width=15)
    label_parameters_row = label_space2_row + 1
    label_parameters.grid(column=4, columnspan=3, row=label_parameters_row)

    button_sample_function = Button(window, text='f. Przykładowa', width=15,
                                    command=lambda: enter_function(entry_formula, sample_function))
    button_sample_function_row = label_parameters_row + 1
    button_sample_function.grid(column=12, columnspan=3, row=button_sample_function_row)
    button_sample_function.anchor(E)

    button_rosenbrock_function = Button(window, text='f. Rosenbrocka', width=15,
                                        command=lambda: enter_function(entry_formula, rosenbrock_function))
    button_rosenbrock_function_row = button_sample_function_row + 1
    button_rosenbrock_function.grid(column=12, columnspan=3, row=button_rosenbrock_function_row)

    button_zangwill_function = Button(window, text='f. Zangwilla', width=15,
                                      command=lambda: enter_function(entry_formula, zangwill_function))
    button_zangwill_function_row = button_rosenbrock_function_row + 1
    button_zangwill_function.grid(column=12, columnspan=3, row=button_zangwill_function_row)

    button_goldstein_price_function = Button(window, text='f. Goldsteina-Price\'a', width=15,
                                             command=lambda: enter_function(entry_formula, goldstein_price_function))
    button_goldstein_price_function_row = button_zangwill_function_row + 1
    button_goldstein_price_function.grid(column=12, columnspan=3, row=button_goldstein_price_function_row)

    button_rastrigin_function = Button(window, text='f. Rastrigina', width=15,
                                       command=lambda: enter_function(entry_formula, rastrigin_function))
    button_rastrigin_function_row = button_goldstein_price_function_row + 1
    button_rastrigin_function.grid(column=12, columnspan=3, row=button_rastrigin_function_row)

    global entry_x1_left
    entry_x1_left = Entry(window, width=10, justify=RIGHT)
    entry_x1_left.insert(0, "-1")
    entry_x1_left_row = label_parameters_row + 1
    entry_x1_left.grid(column=0, columnspan=2, row=entry_x1_left_row)

    label_x1 = Label(window, text="\u2264 x\u2081 \u2264", width=5)
    label_x1_row = entry_x1_left_row
    label_x1.grid(column=2, row=label_x1_row)

    global entry_x1_right
    entry_x1_right = Entry(window, width=10)
    entry_x1_right.insert(0, "1")
    entry_x1_right_row = label_x1_row
    entry_x1_right.grid(column=3, columnspan=2, row=entry_x1_right_row)

    global entry_x2_left
    entry_x2_left = Entry(window, width=10, justify=RIGHT)
    entry_x2_left.insert(0, "-1")
    entry_x2_left_row = entry_x1_right_row + 1
    entry_x2_left.grid(column=0, columnspan=2, row=entry_x2_left_row)

    label_x2 = Label(window, text="\u2264 x\u2082 \u2264", width=5)
    label_x2_row = entry_x2_left_row
    label_x2.grid(column=2, row=label_x2_row)

    global entry_x2_right
    entry_x2_right = Entry(window, width=10)
    entry_x2_right.insert(0, "1")
    entry_x2_right_row = label_x2_row
    entry_x2_right.grid(column=3, columnspan=2, row=entry_x2_right_row)

    global entry_x3_left
    entry_x3_left = Entry(window, width=10, justify=RIGHT)
    entry_x3_left.insert(0, "-1")
    entry_x3_left_row = entry_x2_right_row + 1
    entry_x3_left.grid(column=0, columnspan=2, row=entry_x3_left_row)

    label_x3 = Label(window, text="\u2264 x\u2083 \u2264", width=5)
    label_x3_row = entry_x3_left_row
    label_x3.grid(column=2, row=label_x3_row)

    global entry_x3_right
    entry_x3_right = Entry(window, width=10)
    entry_x3_right.insert(0, "1")
    entry_x3_right_row = label_x3_row
    entry_x3_right.grid(column=3, columnspan=2, row=entry_x3_right_row)

    global entry_x4_left
    entry_x4_left = Entry(window, width=10, justify=RIGHT)
    entry_x4_left.insert(0, "-1")
    entry_x4_left_row = entry_x3_right_row + 1
    entry_x4_left.grid(column=0, columnspan=2, row=entry_x4_left_row)

    label_x4 = Label(window, text="\u2264 x\u2084 \u2264", width=5)
    label_x4_row = entry_x4_left_row
    label_x4.grid(column=2, row=label_x4_row)

    global entry_x4_right
    entry_x4_right = Entry(window, width=10)
    entry_x4_right.insert(0, "1")
    entry_x4_right_row = label_x4_row
    entry_x4_right.grid(column=3, columnspan=2, row=entry_x4_right_row)

    global entry_x5_left
    entry_x5_left = Entry(window, width=10, justify=RIGHT)
    entry_x5_left.insert(0, "-1")
    entry_x5_left_row = entry_x4_right_row + 1
    entry_x5_left.grid(column=0, columnspan=2, row=entry_x5_left_row)

    label_x5 = Label(window, text="\u2264 x\u2085 \u2264", width=5)
    label_x5_row = entry_x5_left_row
    label_x5.grid(column=2, row=label_x5_row)

    global entry_x5_right
    entry_x5_right = Entry(window, width=10)
    entry_x5_right.insert(0, "1")
    entry_x5_right_row = label_x5_row
    entry_x5_right.grid(column=3, columnspan=2, row=entry_x5_right_row)

    label_iteration = Label(window, text="Ilość iteracji:", width=10)
    label_iteration_row = label_parameters_row + 1
    label_iteration.grid(column=6, columnspan=2, row=label_iteration_row)
    label_iteration.config(anchor=E)

    global entry_iteration
    entry_iteration = Entry(window, width=15)
    entry_iteration.insert(0, "100")
    entry_iteration_row = label_iteration_row
    entry_iteration.grid(column=8, columnspan=3, row=entry_iteration_row)

    label_s = Label(window, text="Populacja:", width=10)
    label_s_row = entry_iteration_row + 1
    label_s.grid(column=6, columnspan=2, row=label_s_row)
    label_s.config(anchor=E)

    global entry_s
    entry_s = Entry(window, width=15)
    entry_s.insert(0, "50")
    entry_s_row = label_s_row
    entry_s.grid(column=8, columnspan=3, row=entry_s_row)

    label_f = Label(window, text="F:", width=10)
    label_f_row = entry_s_row + 1
    label_f.grid(column=6, columnspan=2, row=label_f_row)
    label_f.config(anchor=E)

    global entry_f
    entry_f = Entry(window, width=15)
    entry_f.insert(0, "0.5")
    entry_f_row = label_f_row
    entry_f.grid(column=8, columnspan=3, row=entry_f_row)

    label_cr = Label(window, text="CR:", width=10)
    label_cr_row = entry_f_row + 1
    label_cr.grid(column=6, columnspan=2, row=label_cr_row)
    label_cr.config(anchor=E)

    global entry_cr
    entry_cr = Entry(window, width=15)
    entry_cr.insert(0, "0.1")
    entry_cr_row = label_cr_row
    entry_cr.grid(column=8, columnspan=3, row=entry_cr_row)

    button_calculate = Button(window, text='Oblicz', command=lambda: calculate(entry_formula))
    button_calculate_row = label_x5_row + 1
    button_calculate.grid(column=4, columnspan=3, row=button_calculate_row)

    global label_variable_value
    label_variable_value = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
    label_xn_row = button_calculate_row + 1
    # tabela ze zmiennymi
    label_x1 = Label(window, textvariable=label_variable_value[0], width=15)
    label_x1.grid(column=0, columnspan=3, row=label_xn_row)
    label_x1.config(anchor=W)
    label_x2 = Label(window, textvariable=label_variable_value[1], width=15)
    label_x2.grid(column=0, columnspan=3, row=label_xn_row + 1)
    label_x2.config(anchor=W)
    label_x3 = Label(window, textvariable=label_variable_value[2], width=15)
    label_x3.grid(column=0, columnspan=3, row=label_xn_row + 2)
    label_x3.config(anchor=W)
    label_x4 = Label(window, textvariable=label_variable_value[3], width=15)
    label_x4.grid(column=0, columnspan=3, row=label_xn_row + 3)
    label_x4.config(anchor=W)
    label_x5 = Label(window, textvariable=label_variable_value[4], width=15)
    label_x5.grid(column=0, columnspan=3, row=label_xn_row + 4)
    label_x5.config(anchor=W)

    global label_result_value
    label_result_value = StringVar()
    label_result = Label(window, textvariable=label_result_value, width=15)
    label_result.grid(column=0, columnspan=3, row=label_xn_row + 5)
    label_result.config(anchor=W)


class InvalidVariableError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class InvalidBoundsError(Exception):
    pass


def check_variables(variables_name):
    for variable in variables_name:
        is_proper = re.match('x[1-' + str(max_number_of_variables) + ']\\b', variable)
        if is_proper:
            pass
        else:
            raise InvalidVariableError()


def get_bounds():
    bounds_value = [[], [], [], [], []]
    bounds_key = ['x1', 'x2', 'x3', 'x4', 'x5']
    try:
        bounds_value[0].append(float(entry_x1_left.get()))
        bounds_value[0].append(float(entry_x1_right.get()))

        bounds_value[1].append(float(entry_x2_left.get()))
        bounds_value[1].append(float(entry_x2_right.get()))

        bounds_value[2].append(float(entry_x3_left.get()))
        bounds_value[2].append(float(entry_x3_right.get()))

        bounds_value[3].append(float(entry_x4_left.get()))
        bounds_value[3].append(float(entry_x4_right.get()))

        bounds_value[4].append(float(entry_x5_left.get()))
        bounds_value[4].append(float(entry_x5_right.get()))

        bounds = bounds_value

    except ValueError:
        messagebox.showinfo("Błąd", "Niepoprawne wartości ograniczeń")

    return bounds


def get_parameters():  # TODO dodac zczytywanie danych, ewentualnie wywalic blad InvalidParameterError
    parameter_key = ['bounds', 'iterations', 's', 'f', 'cr', 'cr']

    bounds = get_bounds()

    parameters = None
    try:
        iterations = int(entry_iteration.get())
        s = int(entry_s.get())
        f = float(entry_f.get())
        cr = float(entry_cr.get())
        if iterations < 0 or s < 0 or f < 0 or cr < 0 or s < 4:
            raise InvalidParameterError
        if bounds[0][0] > bounds[0][1] or bounds[1][0] > bounds[1][1] or bounds[2][0] > bounds[2][1] or bounds[3][0] > \
                bounds[3][1] or bounds[4][0] > bounds[4][1]:
            raise InvalidBoundsError
        parameters = dict(zip(parameter_key, [bounds, iterations, s, f, cr]))
    except ValueError:
        messagebox.showinfo("Błąd", "Niepoprawne wartości parametrów")
    except InvalidParameterError:
        messagebox.showinfo("Błąd",
                            "Wartości parametrów: Ilość iteracji, Populacja, F i CR \n muszą być dodatnie, a populacja conajmniej równa 4")
    except InvalidBoundsError:
        messagebox.showinfo("Błąd", "Lewe ograniczenie musi być mniejsze niż prawe")
    return parameters


def clear_label_variables_and_result():
    for text in label_variable_value:
        text.set('')
    label_result_value.set('')


def print_result(variables_name, variables_value, result_value):
    clear_label_variables_and_result()
    variables_dict = dict(zip(variables_name, variables_value))
    variables_name = sorted(variables_name)
    i = 0
    for variable_name in variables_name:
        label_variable_value[i].set(variable_name + ' = ' + str(round(variables_dict.get(variable_name), 5)))
        i += 1
    label_result_value.set('min f(x) = ' + str(round(result_value, 5)))


def calculate(entry_obj):
    formula_text = entry_obj.get()
    parser = Parser()
    if len(formula_text) > 1:  # bo puste jest jako 1
        try:  # tu probuje obliczac
            formula = parser.parse(formula_text)
            formula_variables = formula.variables()
            check_variables(formula_variables)  # sprawdzenie czy zmienne to tylko x1,x2,...,itp
            parameters = get_parameters()
            if parameters is not None:
                bounds = parameters.get('bounds')
                iterations = parameters.get('iterations')
                s = parameters.get('s')  # TODO populacja musi byc >=4
                f = parameters.get('f')
                cr = parameters.get('cr')
                # uruchomienie algorytmu
                x = de_algorithm(formula, formula_variables, bounds, iterations, s, f, cr)
                # wydruk wynikow
                result_value = formula.evaluate(dict(zip(formula_variables, x)))
                print_result(formula_variables, x, result_value)

        # obsluga bledow
        except ValueError:
            clear_label_variables_and_result()
            messagebox.showinfo("Błąd",
                                "Niepoprawnie wprowadzona funkcja")
        except ZeroDivisionError:
            clear_label_variables_and_result()
            messagebox.showinfo("Błąd", "Dzielenie przez 0")
        except InvalidVariableError:
            clear_label_variables_and_result()
            messagebox.showinfo("Błąd",
                                "Niedozwolona zmienna."
                                "\nZmienna musi być z zakresu x1-x" + str(max_number_of_variables))
        except InvalidParameterError:
            clear_label_variables_and_result()
            messagebox.showinfo("Błąd",
                                "Niepoprawna wartość parametru")
    else:
        messagebox.showinfo("Błąd", "Brak funkcji celu")


init_window()
mainloop()
