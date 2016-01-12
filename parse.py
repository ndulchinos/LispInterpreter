def parse(input, start, stop):
#return ast of object between ( and )
    index = start
    ast_result = []
    while index<stop:
        cur_char = input[index]
        if cur_char == '(':
            s = find_next_paren(input, index)
            ast_result.append(parse(input, index + 1, s))
            index = s
        elif cur_char == ';':
            index = skip_comment(input, index)
        elif cur_char == '"':
            token, index = get_string(input, index)
            assert(index != -1)
            ast_result.append(token)
        else:
            s = get_next_tok(input, index)
            assert(s != -1)
            token = input[index:s]
            if is_op(token):
                ast_result.append(token)
            elif token.isdigit():
                ast_result.append(int(token))
                index = s
            elif token.isalnum():
                ast_result.append(token)
                index = s
            elif token == "#t":
                ast_result.append(True)
                index = s
            elif token == "#f":
                ast_result.append(False)
                index = s
        index += 1
    return ast_result

def is_op(char):
#is char an operator?
    ops = ['+', '-', '*', '/', "%", ">", "<", "="]
    for op in ops:
        if char == op:
            return True
    return False

def skip_comment(input, pos):
#finds next new line position
    while pos<len(input):
        if input[pos] == '\n':
            return pos
        pos += 1
    return -1

def get_next_tok(input, pos):
#return the position of next space/new line
    white_space = [' ', '\n', ')', ';']
    while pos<len(input):
        cur_char = input[pos]
        for i in white_space:
            if cur_char == i:
                return pos
        pos += 1
    return -1

def get_string(input, first):
#return string, index of closing quote
    assert(input[first] == '"')
    index = first
    while index<len(input):
        index += 1
        if input[index] == '"':
            token = input[(first + 1):index]
            return (token, index)
    return ("", -1)

def find_next_paren(input, first):
#return the index of the closing paren
    assert(input[first] == '(')
    open = 1
    index = first
    while index<len(input):
        index += 1
        if input[index] == '(':
            open += 1
        elif input[index] == ')':
            open -= 1
            if open == 0:
                return index 
    return -1    
