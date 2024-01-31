import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import integrate
import sympy as sp

# рисуем график
def grafic_trapizoidal(a, b, func, n):
    x = np.linspace(a, b, 100)
    y = np.vectorize(lambda x: float(calculate_expression(func, x)))(x)
    plt.plot(x, y, label=func, color='blue')
    for i in range(1, n + 1):
        x_trap = [a + (i-1)*(b-a)/n, a + i*(b-a)/n, a + i*(b-a)/n, a + (i-1)*(b-a)/n, a + (i-1)*(b-a)/n]
        y_trap = [0, 0, float(calculate_expression(func, a + i*(b-a)/n)), float(calculate_expression(func, a + (i-1)*(b-a)/n)), 0]
        plt.plot(x_trap, y_trap, color='orange', alpha=0.5)
    plt.title('trapezoidal grafic')
    plt.xlabel('x')
    plt.ylabel('y')
    # Добавление легенды
    plt.legend()   

    # Отображение графика
    plt.show()

# Преобразовать пи на 180
def replace_pi(value):
    return value.replace('pi', str(180))

# калькулятор который считает интеграл
def calculate_integral(func, a, b):
    def wrapper(x):
        return calculate_expression(func, x)

    result, error = integrate.quad(wrapper, a, b)
    return result

# калькулятор который находит производную
def calculate_derivative(expression_str):
    x = sp.symbols('x')
    try: 
        expression = sp.sympify(expression_str) # преобразавание в класс
        derivative = sp.diff(expression, x) # нахождение производного
        derivative = sp.diff(derivative, x) # also derevative
        
        return str(derivative) # переобразование в строку от класса 
    except Exception as e:
        return f"Ошибка: {str(e)}"

# ввод может быть например 2х+1 и наша функция calculate_expression не понимает что надо делать между 2 и х п этому мы ее отредактируем на 2*х+1
def function_edit(f):
    i = 0
    s = ''
    while i < len(f):
        if f[i] == 'x':# ищем Х
            if i != 0:  # проверяем не первый ли индекс у Х
                if f[i-1].isdigit(): # проверка число ли то что стоит перед Х
                    s = s + '*' # добавляем перед Х умножение
        if f[i] == 'p': # когда пользователь вводит лимиты может написать 2pi и опять же наш калькулятор это не понимает по этому испровляем на 2*pi
            if i != 0:   # опять же проверяем не первый ли индекс у Pi
                if f[i-1].isdigit(): # проверка число ли то что стоит перед Pi
                    s = s + '*' # добавляем перед Pi умножение
        s = s + f[i]
        i = i + 1
    return s 

# калькулятор который считает математические задачи в виде строка
def calculate_expression(expression, x):
    try:
        expression = expression.replace('sin', 'math.sin(math.radians') # меняем sin на math.sin(math.radians( потому что функция eval принимает в таком формате
        expression = expression.replace('cos', 'math.cos(math.radians')
        expression = expression.replace('^', '**') # та же тема, он не принимает символ ^ потому что у нас оператор степени это ** 
        if 'math' not in expression: # если у нас в строке есть слово math то мы должны поставить еще одну скобку в конец, потому что у нас не будет открыта от math.sin(
            expression = expression.replace('x', f'({str(x)})') # а скобка нужна для того чтоб если у нас цифра отрицательная то он должен быть в скобке
        else:
            expression = expression.replace('x', f'({str(x)}))') 
        result = eval(expression) # та функция который вернет результат
        return result
    except Exception as e:
        return f"Ошибка: {str(e)}"

# находим субинтервалы
def a_mean(x, lower, n):
    a_meaning = []
    for i in range(n):
        a_meaning.append(lower)
        lower = x + lower
    a_meaning.append(lower)
    return a_meaning

# сумма всех значении субинтервалов
def sum_up(a):
    total_sum = 0
    for i in range(len(a)):
        total_sum += a[i]
    return total_sum

# формула Trapezoidal, который умножаем субинтервалы в 2 кроме двух крайних
def Trapezoidal_res(a):
    trapezoidal_res = a.copy()

    for i in range(1, len(trapezoidal_res) - 1):
        trapezoidal_res[i] *= 2

    return trapezoidal_res

# формула Simpson, который умножаем суинтервалы 4,2,4,2...2,4 кроме двух крайних
def Simpson_res(a):
    simpson_res = a.copy()
    for i in range(1, len(simpson_res) - 1, 2):
        simpson_res[i] *= 4

    for i in range(2, len(simpson_res) - 1, 2):
        simpson_res[i] *= 2

    return simpson_res

# мы тут все субинтервалы подставляем в функцию интегрл
def result(a, function):
    for i in range(0, len(a)):
        a[i] = calculate_expression(function, a[i])
    return a
    

if __name__ == "__main__":
    lower = input("Enter lower limit (a): ")
    upper = input("Enter upper limit (b): ")
    upper = float(calculate_expression(replace_pi(function_edit(upper)), 0)) # тут мы с перво редактируем нашу функцию, Pi заменяем на 180, и если есть перед ним число то мы умножаем на нее 
    lower = float(calculate_expression(replace_pi(function_edit(lower)), 0)) # тоже самое
    n = int(input("Enter number of subintervals (n): "))
    function = input("Enter function: ")
    function = function_edit(function) # мы редактируем функцию
    derivative = calculate_derivative(function) # создаем переменную который будет хранить себе вторую производную фнукции
    x = (upper - lower) / n # делта Х
    a = a_mean(x, lower, n) # субинтервалы  
    m = calculate_expression(derivative, upper) # находим М
    Et = round((float(m) * (upper - lower)**3) / (12 * n**2), 4) # находим Еррор трапезойдал
    Es = round((float(m) * (upper - lower)**5) / (180 * n**4), 4) # находим Еррор симпсон
    print('\na = ', end=' ')
    for value in a:
        print(value, end=', ')  # выводим все субинтервалы
    print('\n')
    a = result(a, function) # обнавляем субинтервалы подставляя на фнукцию интеграл
    a_trapezoidal = Trapezoidal_res(a) # подставляем на формулу Трапезойдал
    a_simpson = Simpson_res(a) # подставляем на формулу Симпсон
    trapezoidal_sum = sum_up(a_trapezoidal) # находим сумму значении Трапезойдала
    simpson_sum = sum_up(a_simpson) # находим сумму значении Симпсон
    final_result_trapezoidal = round(x / 2 * trapezoidal_sum, 4) # подставляем на формулу 
    final_result_simpson = round(x / 3 * simpson_sum, 4) # подставляем на формулу 
    true_value = round(calculate_integral(function, lower, upper), 4) # находим интеграл
    
    
    # вывод
    print(f'a) Trapezoidal result: {final_result_trapezoidal}')
    print(f'Et <= {Et}')
    Et = round(true_value - final_result_trapezoidal, 4)
    if Et < 0: # проверка если число отрицательный то мы просто умножаем на -1 
        Et = Et * (-1)
    res_T = (Et/true_value) * 100 # процент ошибки
    print(f'b) |Et| = {Et}')
    print(f'c) Final trapezoidal: {int(res_T)}%\n')
    print(f'a) Simpson result: {final_result_simpson}')
    print(f'Es <= {Es}')
    Es = round(true_value - final_result_simpson, 4) 
    if Es < 0: # проверка если число отрицательный то мы просто умножаем на -1 
        Es = Es * (-1)
    res_S = (Es/true_value) * 100 # процент ошибки 
    print(f'b) |Es| = {Es}')
    print(f'c) Final simpson: {int(res_S)}%')

    grafic_trapizoidal(lower, upper, function, n)
