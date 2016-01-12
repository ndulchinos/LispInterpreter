import argparse
from parse import parse
from evaluate import evaluate_ast

parser = argparse.ArgumentParser(description='lisp interpreter')
parser.add_argument('file')
args = parser.parse_args()

f = open(args.file)
inp = f.read()
f.close()

ast = parse(inp, 0, len(inp))

for element in ast:
    x = evaluate_ast(element)


