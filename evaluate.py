class mode:
    none = 0
    add = 1
    sub = 2
    mul = 3
    div = 4
    iff = 5
    less = 6
    more = 7
    eq = 8
    define = 9
    fcall = 10
    prnt = 11

class env:
    exps = {"1" : "1"}
    reserved = {"+" : "1",
                "-" : "1",
                "*" : "1",
                "/" : "1",
                "if" : "1",
                "define": "1",
                "print": "1"}

def evaluate_ast(input):
#take ast, return value
    m = mode.none
    acc = 0
    acc_init = False
    
    m = handle_first(input)

    if m == mode.none:
        if isinstance(input, list):
            if len(input) == 1:
                return input[0]
        return input
    elif m == mode.fcall:
        return handle_call(input[0], input[1:])
    elif m == mode.prnt:
        print(evaluate_ast(input[1]))
        return True

    for idx, element in enumerate(input):
        if idx == 0:
            continue

        if isinstance(element, list):
            e = evaluate_ast(element)
            if isinstance(e, int):
                element = e
        
        if isinstance(element, bool):
            if m == mode.iff:
                if element:
                    return evaluate_ast(input[idx+1])
                else:
                    return evaluate_ast(input[idx+2])
            else:
                return element

        if isinstance(element, int):
            if not acc_init:
                acc_init = True
                acc = element
                continue
            if m == mode.add:
                acc += element
            elif m == mode.sub:
                acc -= element
            elif m == mode.mul:
                acc *= element
            elif m == mode.less:
                return acc < element
            elif m == mode.more:
                return acc > element
            elif m == mode.eq:
                return acc == element
              
    if arithmetic(m):  
        return acc


def handle_call(name, args):
#return function result of calling (name (args))
    assert(name in env.exps)
    ast = list(env.exps[name])
    replace(ast, ast[0], args)
    return evaluate_ast(ast[1])
    
def replace(input, names, values):
    assert(len(names) == len(values))
    for idx, element in enumerate(input):
        if isinstance(element, list):
            input[idx] = list(input[idx])
            element = input[idx]
            replace(element, names, values)
        elif isinstance(element, str):
            for n, v in zip(names, values):
                if element == n:
                    input[idx] = v

def handle_definition(input):
#return True if successful, False if func already exists
    name = input[1]
    if name in env.exps or name in env.reserved:
        return False
    else:
        env.exps.update({name:input[2:]})
    return True

def handle_first(input):
#return mode
    first = input
    if isinstance(input, list):
        first = input[0]
    if first == "if":
        assert(len(input) == 4)
        return mode.iff
    elif first == "+":
        return mode.add
    elif first == "-":
        return mode.sub
    elif first == "*":
        return mode.mul
    elif first == "/":
        return mode.div
    elif first == "<":
        assert(len(input) == 3)
        return mode.less
    elif first == ">":
        assert(len(input) == 3)
        return mode.more
    elif first == "=":
        assert(len(input) == 3)
        return mode.eq
    elif first == "define":
        assert(len(input) == 4)
        success = handle_definition(input)
        assert(success)
        return mode.define
    elif first == "print":
        assert(len(input) == 2)
        return mode.prnt
    elif first in env.exps:
        return mode.fcall
    else: 
        return mode.none
        
def arithmetic(m):
#return true if m is an arithmatic mode
    if m == mode.add:
        return True
    if m == mode.sub:
        return True
    if m == mode.mul:
        return True
    if m == mode.div:
        return True
    return False
