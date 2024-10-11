from decimal import Decimal, ROUND_HALF_UP


def input_data():
    problem = input("Please enter 'max' if you solve maximization problem"
                    " and 'min' if you solve minimization problem: \n")

    C = list(map(int, input("Enter the vector of coefficients "
                            "of objective function\n").split()))
    variables_num = len(C)
    # Vector of coefficients of objective function

    if problem == 'max':
        for i in range(len(C)):
            C[i] = -C[i]

    A = list()
    # Matrix of coefficients of constraint functions

    n = int(input("Enter the number of constraint functions\n"))
    for i in range(n):
        C.append(0)
        A.append(list(map(int, input("Enter the coefficients of "
                                     "constraint function (without slack variables)\n").split())))
        for j in range(n):
            A[i].append(0)
        A[i][len(C) - 1] = 1

    b = [0]
    b += list(map(int, input("Enter the vector of right-hand side numbers\n").split()))
    # Vector of right-hand side numbers

    accuracy = float(input("Enter the approximation accuracy\n"))
    # Approximation accuracy

    precision = "1." + "0" * int(input("Enter the precision accuracy "
                                       "(how many numbers after the decimal point)\n"))

    return C, A, b, problem, variables_num, accuracy, precision


def find_pivot(col_pivot_index, A, b):
    ratio = [0] * len(A)
    for i in range(len(A)):
        if A[i][col_pivot_index] == 0:
            ratio[i] = -1
            continue
        ratio[i] = b[i + 1] / A[i][col_pivot_index]
    m = max(ratio)
    if m <= 0:
        return -1, -1
    for i in ratio:
        if (i > 0) and (i < m):
            m = i
    row_pivot_index = ratio.index(m)
    pivot_element = A[row_pivot_index][col_pivot_index]
    return pivot_element, row_pivot_index


def transform(C, A, b, row_pivot_index, col_pivot_index, pivot):
    b[row_pivot_index + 1] = b[row_pivot_index + 1] / pivot
    for i in range(len(A[row_pivot_index])):
        A[row_pivot_index][i] = A[row_pivot_index][i] / pivot

    for i in range(len(A)):
        if i == row_pivot_index:
            continue
        coefficient = A[i][col_pivot_index]
        b[i + 1] = b[i + 1] - coefficient * b[row_pivot_index + 1]
        for j in range(len(A[i])):
            A[i][j] = A[i][j] - A[row_pivot_index][j] * coefficient

    coefficient = C[col_pivot_index]
    b[0] = b[0] - b[row_pivot_index + 1] * coefficient
    for i in range(len(C)):
        C[i] = C[i] - A[row_pivot_index][i] * coefficient
    return C, A, b


def find_decision_variables(C, A, b, variables_num):
    decision_variables = [0] * len(C)
    for i in range(len(A[0])):
        one_counter = 0
        zero_counter = 0
        index = 0
        for j in range(len(A)):
            if A[j][i] == 1:
                one_counter += 1
                index = j
            elif A[j][i] == 0:
                zero_counter += 1
            else:
                break
        if (one_counter == 1) and (zero_counter == len(A) - 1):
            decision_variables[i] = b[index + 1]
    return decision_variables[:variables_num]


def solve():
    C, A, b, problem, variables_num, accuracy, precision = input_data()
    while min(C) < 0:
        C_previous = C.copy()
        A_previous = A.copy()
        b_previous = b.copy()
        col_pivot_index = C.index(min(C))
        pivot, row_pivot_index = find_pivot(col_pivot_index, A, b)
        if pivot == -1:
            print("The method is not applicable!")
            return
        C, A, b = transform(C, A, b, row_pivot_index, col_pivot_index, pivot)
        if abs(b_previous[0] - b[0]) < accuracy:
            C = C_previous
            A = A_previous
            b = b_previous
            break
    if problem == "max":
        print("Vector of decision variables: ")
        decision_variables = find_decision_variables(C, A, b, variables_num)
        print([float(Decimal(x).quantize(Decimal(precision))) for x in decision_variables])
        print("Maximum value of objective function: ")
        print(float(Decimal(b[0]).quantize(Decimal(precision), ROUND_HALF_UP)))
    elif problem == "min":
        print("Vector of decision variables: ")
        decision_variables = find_decision_variables(C, A, b, variables_num)
        print([float(Decimal(x).quantize(Decimal(precision), ROUND_HALF_UP)) for x in decision_variables])
        print("Minimum value of objective function: ")
        print(float(Decimal(-b[0]).quantize(Decimal(precision), ROUND_HALF_UP)))


solve()
