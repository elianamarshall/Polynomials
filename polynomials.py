def is_valid_number(num: str) -> bool:
    """
    Returns True if and only if num is represents a valid number.

    >>> is_valid_number("10")
    True
    >>> is_valid_number("-124")
    True
    >>> is_valid_number("12.9")
    True
    >>> is_valid_number("12.9.0")
    False
    >>> is_valid_number("abc")
    False
    """
    split = num.split(".")
    # checks if it is a valid decimal or int
    if len(split) > 2 or not split[0]: 
        return False
    num1 = True
    num2 = True
    # checks if it is a negative number
    if split[0][0] == "-": 
        num1 = split[0][1:].isnumeric()
    else:
        num1 = split[0].isnumeric()
    # checks if the number endsin a "." or is numeric
    if len(split) != 1: 
        num2 = not split[1] or split[1].isnumeric()
    return num1 and num2



def is_valid_term(term: str) -> bool:
    """
    Returns True if and only if num is represents a valid term.

    >>> is_valid_term("44.4x^6")
    True
    >>> is_valid_term("-7x")
    True
    >>> is_valid_term("9.9")
    True
    >>> is_valid_term("7y**8")
    False
    >>> is_valid_term("7x^8.8")
    False
    >>> is_valid_term("7*x^8.8")
    False
    >>> is_valid_term("7x^ 8.8")
    False
    """
    # checks if there is a string in the term
    if " " in term: return False
    # checks if the term is a valid number
    if is_valid_number(term): 
        return True
    # checks if the term is a valid first degree term
    if term.endswith('x') and is_valid_number(term[:-1]): 
        return True
    # checks if the term is a valid term of degree greater than 1
    if 'x^' in term: 
        parts = term.split('x^')
        if len(parts) == 2:
            coef, exponent = parts
            if is_valid_number(coef) and exponent.isdigit() and int(exponent) > 2:
                return True
    return False
        


def approx_equal(x: float, y: float, tol: float) -> bool:
    """
    Returns True if and only if x and y are within tol of each other.

    >>> approx_equal(5, 4, 1)
    True
    >>> approx_equal(5, 3, 1)
    False
    >>> approx_equal(0.999, 1, 0.001)
    True
    >>> approx_equal(0.999, 1, 0.0001)
    False
    """
    return abs(x - y) <= tol



def degree_of(term: str) -> int:
    """
    Returns the degree of term, it is assumed that term is a valid term.

    >>> degree_of("55x^6")
    6
    >>> degree_of("-1.5x")
    1
    >>> degree_of("252.192")
    0
    """
    # checks if it is a term of degree more than 1
    if "x^" in term:
        return int(term.split("x^")[1])
    # checks if it is a first degree term
    elif "x" in term:
        return 1
    else:
    #checks if it is not a variable
        return 0



def get_coefficient(term: str) -> float:
    """
    Returns the coefficient of term, it is assumed that term is a valid term.

    >>> get_coefficient("55x^6")
    55
    >>> get_coefficient("-1.5x")
    -1.5
    >>> get_coefficient("252.192")
    252.192
    """
    return float(term.split("x")[0] if "x" in term else term)



#********************************************
def derive(poly):
    derivative = []
    degree = 1
    for coefficient in poly[1:]:
        derivative.append(coefficient*degree)
        degree += 1
    return derivative

def get_coefficients(terms):
    poly = []
    degree = 0
    for term in terms:
        while degree != degree_of(term):
            poly.append(0)
            degree += 1
        poly.append(get_coefficient(term))
        degree +=1
    return poly

def evaluate(poly, x):
    value = 0
    degree = 0
    for coefficient in poly:
        degree += 1
        value += coefficient * x**degree
    return value
        

if __name__ == "__main__":
    poly_string = input("Please enter a polynomial: ")
    terms = poly_string.strip().split("+")

    valid_poly = True
    for term in terms:
        if not is_valid_term(term):
            valid_poly = False

    while not valid_poly:
        poly_string = input("Incorrect format. Please enter a polynomial: ")
        terms = poly_string.strip().split("+")

        valid_poly = True
        for term in terms:
            if not is_valid_term(term):
                valid_poly = False
            
    poly = get_coefficients(terms)
    derivative = derive(poly)
    current_value = float(input("Please enter a starting point: "))
    tol = float(input("Please enter a tolerance: "))
    
    next_value = current_value - (evaluate(poly, current_value)/evaluate(derivative, current_value))
    while not(approx_equal(current_value, next_value, tol)):
        current_value = next_value
        next_value = current_value - (evaluate(poly, current_value)/evaluate(derivative, current_value))
    print("The polynoimal has a 'zero' approximately at: " + str(next_value))
