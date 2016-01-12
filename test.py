from parse import find_next_paren
from parse import parse
from parse import get_next_tok
from parse import skip_comment
from parse import get_string
from evaluate import evaluate_ast
from evaluate import handle_definition
from evaluate import handle_call
from evaluate import replace
from evaluate import env

test_case_1 = "(   )"
x = find_next_paren(test_case_1, 0)
assert(x == 4)

test_case_2 = "(()())"
x = find_next_paren(test_case_2, 1)
assert(x == 2)

tc3 = "(+ )"
x = get_next_tok(tc3, 1)
assert(x == 2)

test_case_3 = "(* /)"
y = parse(test_case_3, 0, len(test_case_3))
#print(y)
assert(y == [["*", "/"]])

test_case_4 = "(+ - (+))"
y = parse(test_case_4, 0, len(test_case_4))
#print(y)
assert(y == [["+", "-", ["+"]]])

test_case = "(+ n  (- m 2) #t)"
y = parse(test_case, 0, len(test_case))
#print(y)
assert(y == [["+", "n", ["-", "m", 2], True]])

test_case = """
(define fact
   ;; Factorial Function
   (lamda (n)
      (if (eq n 0)
         1 ; Factorial
         (* n (fact (- n 1))))))
"""
y = parse(test_case, 0, len(test_case))
#print(y)
assert(y == [['define', 'fact', ['lamda', ['n'], ['if', ['eq', 'n', 0], 1, ['*', 'n', ['fact', ['-', 'n', 1]]]]]]])

test_case = "(+ 1 2 3)"
y = parse(test_case, 0, len(test_case))
x = evaluate_ast(['+', 1, 2, 3])
#x = evaluate_ast(y)
#print(y)
#print(x)
assert(x == 6)

x = evaluate_ast(['+', 1, 2, ["-", 4, 1]])
assert(x == 6)

x = evaluate_ast(['<', 1, 2])
assert(x)

x = evaluate_ast(['>', 2, 1])
assert(x)

#x = evaluate_ast([1])
#print(x)
#assert(x == 1)

x = evaluate_ast(['if', ['<', 1, 2], 1, 2])
#print(x)
assert(x == 1)

x = evaluate_ast(['=', 1, 2])
assert(x == False)

x = parse("(= 1 2)", 0, 7)
#print(x)
assert(x == [['=', 1, 2]])

x = handle_definition(["define", "1", 2, 3])
assert(x == False)

handle_definition(["define", "id", ["n"], "n"])
l = list(env.exps["id"])
replace(l, ["n"], [1])
assert(l == [[1], 1])
x = handle_call("id", [1])
assert(x == 1)

evaluate_ast(["define", "add", ["a", "b"], ['+', 'a', 'b']])
assert("add" in env.exps) 
l = list(env.exps["add"])
replace(l, ["a", "b"], [1, 2])
assert(l == [[1, 2], ['+', 1, 2]])
x = handle_call("add", [1, 2])
#print(x)
assert(x == 3)

x = evaluate_ast(["add", 1, 2])
#print(x)
assert(x == 3)

evaluate_ast(["define", "foo", ["n"], ["if", ["=", "n", 1], 1, ["+", "n", ["foo", ["-", "n", 1]]]]])
l = list(env.exps["foo"])
#print(l)
x = evaluate_ast(["foo", 3])
#print(x)
assert(x == 6)

x, y = get_string('"ninin nini"', 0)
assert(x == "ninin nini")

print("all tests passed")
