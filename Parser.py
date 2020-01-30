import sys ,re

try:
    file = open(sys.argv[1], "r")
except FileNotFoundError:
    print("File Not found. sorry")
    sys.exit()
except IndexError:
    print("Please specify file name")
    sys.exit()

#regex rules
wordarray = ["else", "if", "int", "return", "void", "while"]
keywords = r'else|if|int|return|void|while'
special = r'\+|\*-|/|<=|>=|==|!=|<|>|=|;|,|\(|\)|\[|\]|\{|\}'
identifier = r'^[a-zA-Z]+'
numbers = r'[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?'
comments = r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)'
error = r'\S'
#lexer

reading = file.read()
comment = re.sub(comments,"",reading)

token = []
i = 0
for line in comment.split("\n"):
    for word in line.split():
        # print(word)
        keyword = re.match(keywords, word)
        specials = re.match(special, word)
        id = re.match(identifier,word)
        number = re.match(numbers, word)
        errors = re.match(error, word)
        if keyword is not None:
            token.append(keyword.group())
        elif specials is not None:
            token.append(specials.group())
        elif id is not None:
            token.append(id.group())
        elif number is not None:
            token.append(number.group())
        elif errors is not None:
            token.append(errors.group())

token.append("$")
def reject():
    print("REJECT")
    sys.exit(0)

def next():
    global i
    i += 1

def eat(*argv):
    for arg in argv:
        print(token[i])
        if token[i] == arg:
            next()
        else:
            reject()
def program():
    dl()
    if token[i] == "$":
        print ("ACCEPT")
    else:
        reject()

def dl():
    declaration()
    declerationlistprime()

def declerationlistprime():
    if token[i] == "int" or token [i] == "void":
        declaration()
        declerationlistprime()
    elif token[i] == "$":
        return
    else:
        return
def declaration():
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha:
        next()
        if token[i] == ";":
            next()
        elif token [i] == "(":
            next()
            params()
            if token[i] == ")":
                next()
                compoundstmt()
            else:
                reject()
        elif token[i] == "[":
            next()
            if token[i].isnumeric():
                next()
                if token[i] == "]":
                    next()
                    eat(";")
                else:
                    reject()
            else:
                reject()
        else:
            reject()
    else:
        reject()

def var_declaration():
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha:
        next()
    else:
        reject()
    if token[i] == ";":
        next()
    elif token[i] == "[":
        next()
        if token[i].isnumeric():
            next()
            if token[i] == "]":
                next()
                eat(";")
            else:
                reject()
        else:
            reject()
    else:
        reject()

# def id():
#     return


def type_specifier():
    if token[i] == "int" or token[i] == 'void':
        next()
    else:
        return

def fun_declaration():
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha:
        next()
    else:
        return
    eat("(")
    params()
    eat(")")
    compoundstmt()

def params():
    if token[i] == "int":
        paramslist()
    elif token[i] == "void":
        next()  # Accept void
        return
    else:
        reject()

def paramslist():
    param()
    paramslistprime()

def paramslistprime():
    if token[i] == ",":
        next()
        param()
        paramslistprime()
    elif token[i] == ")":
        return
    else:
        return

def param():
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha:
        next()
    else:
        return
    if token[i] == "[":
        next()
        eat("]")
    else:
        return

# def idprime():
#     return

def compoundstmt():
    if token[i] == "{":
        next()
    else:
        return
    local_declaration()
    statement_list()
    eat("}")

def local_declaration():
    ldprime()

def ldprime():
    if token[i] == "int" or token[i] == 'void':
        var_declaration()
        local_declaration()
    else:
        return

def statement_list():
    statement_listprime()

def statement_listprime():
    if token[i] not in wordarray and token[i].isalpha:
        statement()
        statement_listprime()
    elif token[i].isnumeric():
        statement()
        statement_listprime()
    elif token[i] == "(" or token[i] == ";" or token[i] == "{" or token[i] == "if" or token[i] == "while" or token[i] == "return":
        statement()
        statement_listprime()
    elif token[i] == "}":
        return
    else:
        return

def statement():
    if token[i] not in wordarray and token[i].isalpha:
        expression_stmt()
    elif token[i].isnumeric():
        expression_stmt()
    elif token[i] == "(" or token[i] == ";":
        expression_stmt()
    elif token[i] == "{":
        compoundstmt()
    elif token[i] == "if":
        selection_stmt()
    elif token[i] == "while":
        iteration()
    elif token[i] == "return":
        return_stmt()
    else:
        reject()

def expression_stmt():
    if token[i] not in wordarray and token[i].isalpha:
        expression()
        eat(";")
    elif token[i].isnumeric():
        expression()
        eat(";")
    elif token[i] == "(":
        expression()
        eat(";")
    elif token[i] == ";":
        next()
    else:
        reject()


def selection_stmt():
    if token[i] == "if":
        next()
    else:
        return
    eat("(")
    expression() #CHECK LATER
    eat(")")
    statement()     #CHECK LATER
    if token[i] == "else":
        next()
        statement()
    else:
        return

# def elseprime():
#     return

def iteration():
    if token[i] == "while":
        next()
    else:
        return
    eat("(")
    expression()        #CHECK LATER
    eat(")")
    statement()

def return_stmt():
    if token[i] == "return":
        next()
    else:
        return
    if token[i] == ";":
        next()
        return
    elif token[i] not in wordarray and token[i].isalpha:
        expression()
        eat(";")
    elif token[i].isnumeric():
        expression()
        eat(";")
    elif token[i] == "(":
        expression()
        eat(";")
    else:
        reject()

def expression():
    if token[i] not in wordarray and token[i].isalpha:
        next()
        expprime()
    elif token[i] == "(":
        next()
        expression()
        if token[i] == ")":
            next()
            termprime()
            additiveprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                additive_expression()
            elif token[i] == "+" or token[i] == "-":
                additiveprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    additive_expression()
                    #504
            else:
                return
        else:
            reject()
    elif token[i].isnumeric():
        next()
        termprime()
        additiveprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            additive_expression()
        elif token[i] == "+" or token[i] == "-":
            additiveprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                additive_expression()
                #527
        else:
            return
    else:
        reject()

def expprime():
    if token[i] == "=":
        next()
        expression()
    elif token[i] == "[":
        next()
        expression()
        if token[i-1] == "[":
            reject()
        if token[i] == "]":
            next()
            if token[i] == "=":
                next()
                expression()
            elif token[i] == "*" or token[i] == "/":
                termprime()
                additiveprime()
                if token == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    additive_expression()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                additiveprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    additive_expression()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                additive_expression()
            else:
                return
        else:
            reject()
    elif token[i] == "(":
        next()
        args()
        if token[i] == ")":
            next()
            if token[i] == "*" or token[i] == "/":
                termprime()
                additiveprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    additive_expression()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                additiveprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    additive_expression()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                additive_expression()
            else:
                return
        else:
            reject()
    elif token[i] == "*" or token[i] == "/":
        termprime()
        additiveprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            additive_expression()
        else:
            return
    elif token[i] == "+" or token[i] == "-":
        additiveprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            additive_expression()
        else:
            return
    elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        additive_expression()
    else:
        return
def var():
    if token[i] not in wordarray and token[i].isalpha:
        next()
    else:
        return
    if token[i] == "[":
        next()
        expression()
        eat("]")
    else:
        return

# def varprime():
#     return

def simple():
    additive_expression()
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        additive_expression()
    else:
        return

def relop():
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        next()
    else:
        return

def additive_expression():
    term()
    additiveprime()

def additiveprime():
    if token[i] == "+" or token[i] == "-":
        addop()
        term()
        additiveprime()
    else:
        return

def addop():
    if token[i] == "+" or token[i] == "-":
        next()
    else:
        return

def term():
    factor()
    termprime()

def termprime():
    if token[i] == "*" or token[i] == "/":
        mulop()
        factor()
        termprime()
    else:
        return

def mulop():
    if token[i] == "*" or token[i] == "/":
        next()
    else:
        return

def factor():
    if token[i] not in wordarray and token[i].isalpha():
        next()
        if token[i] == "[":
            next()
            expression()
            if token[i] == "]":
                next()
            else:
                return
        elif token[i] == "(":
            next()
            args()
            if token[i] == ")":
                next()
            else:
                return
        else:
            return
    elif token[i].isnumeric():
        next()
    elif token[i] == "(":
        next()
        expression()
        if token[i] == ")":
            next()
        else:
            return
    else:
        reject()

def call():
    if token[i] not in wordarray and token[i].isalpha:
        next()
        if token[i] == "(":
            next()
            args()
            eat(")")
        else:
            reject()
    else:
        return

def args():
    if token[i] not in wordarray and token[i].isalpha():
        arg_list()
    elif token[i].isnumeric():
        arg_list()
    elif token[i] == "(":
        arg_list()
    elif token[i] == ")":
        return
    else:
        return

def arg_list():
    expression()
    arg_listprime()

def arg_listprime():
    if token[i] == ",":
        next()
        expression()
    elif token[i] == ")":
        return
    else:
        return

program()