from decimal import Decimal, ROUND_HALF_UP

def input_data():
    C = list(map(int, input("Enter the vector of coefficients "
                            "of objective function\n").split()))
    # Vector of coefficients of objective function

    A = list()
    # Matrix of coefficients of constraint functions

    n = int(input("Enter the number of constraint functions\n"))
    for i in range(n):
        A.append(list(map(int, input("Enter the coefficients of "
                                     "constraint function\n").split())))

    b = [0]
    b += list(map(int, input("Enter the vector of right-hand side numbers\n").split()))
    # Vector of right-hand side numbers

    accuracy = int(input("Enter the approximation accuracy\n"))
    # Approximation accuracy
    precision = "1." + "0" * accuracy

    return C, A, b, precision

def find_pivot(col_pivot_index, A, b, precision):
    ratio = [0] * len(A)
    for i in range(len(A)):
        ratio[i] = Decimal(str(b[i + 1] / A[i][col_pivot_index])).quantize(Decimal(precision), ROUND_HALF_UP)
    m = max(ratio)
    for i in ratio:
        if (i > 0) and (i < m):
            m = i
    row_pivot_index = ratio.index(m)
    pivot_element = A[row_pivot_index][col_pivot_index]
    return pivot_element, row_pivot_index

def transform(C, A, b, row_pivot_index, col_pivot_index, pivot, precision):

    b[row_pivot_index] = Decimal(str(b[row_pivot_index] / pivot)).quantize(Decimal(precision), ROUND_HALF_UP)
    for i in range(len(A[row_pivot_index])):
        A[row_pivot_index][i] = Decimal(str(A[row_pivot_index][i] / pivot)).quantize(Decimal(precision), ROUND_HALF_UP)
        
    for i in range(len(A)):
        if i == row_pivot_index:
            continue
        coefficient = A[i][col_pivot_index]
        b[i + 1] = b[i + 1] - coefficient * b[row_pivot_index]
        for j in range(len(A[i])):
            A[i][j] = (Decimal(str(A[i][j] - A[row_pivot_index][j] * coefficient))
                       .quantize(Decimal(precision), ROUND_HALF_UP))

    coefficient = C[col_pivot_index]
    b[0] = b[row_pivot_index] * coefficient
    for i in range(len(C)):
        C[i] = (Decimal(str(C[i] - A[row_pivot_index][i] * coefficient))
                .quantize(Decimal(precision), ROUND_HALF_UP))
    return C, A, b


def solve():
    C, A, b, precision = input_data()
    while min(C) < 0:
        col_pivot_index = C.index(min(C))
        pivot, row_pivot_index = find_pivot(col_pivot_index, A, b, precision)
        C, A, b = transform(C, A, b, row_pivot_index, col_pivot_index, pivot, precision)
    print("Vector of coefficients of objective function: ")
    print(C)
    print("\n")
    print("Maximum value of objective function: ")
    print(b[0])

solve()