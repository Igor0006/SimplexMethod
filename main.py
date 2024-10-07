from decimal import Decimal

def input_data():
    C = list(map(int, input("Enter the vector of coefficients"
                            "of objective function").split()))
    # Vector of coefficients of objective function

    A = list()
    # Matrix of coefficients of constraint functions

    n = int(input("Enter the number of constraint functions"))
    for i in range(n):
        A.append(list(map(int, input("Enter the coefficients of "
                                     "constraint function"))))

    b = list(map(int, input("Enter the vector of right-hand side numbers").split()))
    # Vector of right-hand side numbers

    accuracy = int(input("Enter the approximation accuracy"))
    # Approximation accuracy
    precision = "1." + "0" * accuracy

    return C, A, b, precision

def find_ratio_vector(pivot_index, constraint, precision):
    # print(number.quantize(Decimal("1.00"), ROUND_HALF_UP))
    return list()

def solve():
    C, A, b, precision = input_data()
    pivot_index = C.index(min(C))
    ratio = find_ratio_vector(pivot_index, A, precision)
