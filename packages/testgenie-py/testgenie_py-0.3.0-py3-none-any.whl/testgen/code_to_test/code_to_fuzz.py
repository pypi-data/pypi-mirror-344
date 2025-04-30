def random_fuzz_code(x: int, y: int) -> int:
    result = x
    if x < y:
        result += y
    else:
        result -= y
    return result


def bin_and(a: bool, b: bool) -> bool:
    if a == True:
        if b == True:
            return True
        else:
            return False
    else:
        return False


def pos_or_neg(i: int):
    if i > 0:
        sgn = 1
    else:
        sgn = -1
    if sgn > 0:
        return 1
    elif sgn < 0:
        return -1
    # else sgn == 0
    # no return here


def int_even(x: int):
    if x % 2 == 0:
        return True
    else:
        return False

def http_code(code: int) ->str:
    if code < 100 or code > 599:
        return 'invalid'
    elif 100 <= code < 200:
        return 'informational'
    elif 200 <= code < 300:
        return 'success'
    elif 300 <= code < 400:
        return 'redirection'
    elif 400 <= code < 500:
        return 'client error'
    else:
        return 'server error'
    
def add_or_subtract(x: int, y: int) ->int:
    result = x
    if x < y:
        result += y
    else:
        result -= y
    return result
    
def bin_and_bad_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return True
        else:
            return True
    else:
        if b == True:
            return True
        else:
            return False


def bin_nand_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return False
        else:
            return True
    else:
        if b == True:
            return True
        else:
            return True


def bin_nor_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return False
        else:
            return False
    else:
        if b == True:
            return False
        else:
            return True


def bin_or_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return True
        else:
            return True
    else:
        if b == True:
            return True
        else:
            return False


def bin_or_bad_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return False
        else:
            return False
    else:
        if b == True:
            return False
        else:
            return True


def bin_xor_generated_function(a: bool, b: bool):
    if a == True:
        if b == True:
            return False
        else:
            return True
    else:
        if b == True:
            return True
        else:
            return False


def mux_generated_function(c1: bool, c2: bool, x0: bool, x1: bool, x2: bool, x3: bool):
    if c1 == True:
        if c2 == True:
            if x0 == True:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return True
                        else:
                            return True
                else:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return True
                        else:
                            return True
            else:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return False
                        else:
                            return False
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
                else:
                    if x2 == True:
                        if x3 == True:
                            return False
                        else:
                            return False
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
        else:
            if x0 == True:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return True
                        else:
                            return True
                else:
                    if x2 == True:
                        if x3 == True:
                            return False
                        else:
                            return False
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
            else:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return True
                        else:
                            return True
                else:
                    if x2 == True:
                        if x3 == True:
                            return False
                        else:
                            return False
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
    else:
        if c2 == True:
            if x0 == True:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
                else:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
            else:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
                else:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return True
                    else:
                        if x3 == True:
                            return False
                        else:
                            return False
        else:
            if x0 == True:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return False
                    else:
                        if x3 == True:
                            return True
                        else:
                            return False
                else:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return False
                    else:
                        if x3 == True:
                            return True
                        else:
                            return False
            else:
                if x1 == True:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return False
                    else:
                        if x3 == True:
                            return True
                        else:
                            return False
                else:
                    if x2 == True:
                        if x3 == True:
                            return True
                        else:
                            return False
                    else:
                        if x3 == True:
                            return True
                        else:
                            return False