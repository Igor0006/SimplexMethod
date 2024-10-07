from decimal import Decimal, ROUND_HALF_UP

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

def find_pivot(pivot_index, A, b, precision):
    ratio = list()
    for i in range(len(A)):
        ratio[i] = (b[i] / A[i][pivot_index]).quantize(Decimal(precision), ROUND_HALF_UP)
    m = max(ratio)
    for i in ratio:
        if (i > 0) and (i < m):
            m = i
    ratio_pivot = ratio.index(m)
    pivot_element = A[ratio_pivot][pivot_index]
    return pivot_element, ratio_pivot

def transform(C, A, b, ratio_pivot, pivot, precision):
    b[ratio_pivot] = (b[ratio_pivot] / pivot).quantize(Decimal(precision), ROUND_HALF_UP)
    for i in range(len(b)):
        if i == ratio_pivot:
            continue
        b[i] = b[i] - b[ratio_pivot]
    for i in range(len(A[ratio_pivot])):
        A[ratio_pivot][i] = (A[ratio_pivot][i] / pivot).quantize(Decimal(precision), ROUND_HALF_UP)
    for i in range(len(A)):
        if i == ratio_pivot:
            continue
        for j in range(len(A[i])):
            A[i][j] = A[i][j] - A[ratio_pivot][j]
    for i in range(len(C)):
        C[i] = C[i] - A[ratio_pivot][i]
    return C, A, b


def solve():
    C, A, b, precision = input_data()
    pivot_index = C.index(min(C))
    while pivot_index < 0:
        pivot, ratio_pivot = find_pivot(pivot_index, A, b, precision)
        C, A, b = transform(C, A, b, ratio_pivot, pivot, precision)
        pivot_index = C.index(min(C))
    print("Vector of coefficients of objective function:")
    print(C)
    print("Maximum value of objective function:")
    print(b[0])