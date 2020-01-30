import sys, re

try:
    file = open("test.txt", "r")
except FileNotFoundError:
    print("File Not found. sorry")
    sys.exit()
except IndexError:
    print("Please specify file name")
    sys.exit()
wordarray = ["else", "if", "int", "return", "void", "while"]
keywords = "[a-z]+"
numbersRegex = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"
symRegex = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"
errorRegex = "\S"
comments = r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)'

reading = file.read()
comment = re.sub(comments, "", reading)
token = []
i = 0
for line in comment.split("\n"):
    regex = "(%s)|(%s)|(%s)|(%s)" % (keywords, numbersRegex, symRegex, errorRegex)
    for word in re.findall(regex, line):
        if word[0]:
            if word[0] in keywords:
                token.append(word[0])
            else:
                token.append(word[0])
        elif word[1]:
            token.append(word[1])
        elif word[5]:
            token.append(word[5])
        elif word[6]:
            token.append(word[6])
token.append("$")

q = 1
t = 0
currfunc = 0
incurrfun = 0
inexp = 0
ifnum = 0
iniflist = 0
ifbr = 0
elsebr = 0
dubcheck = 0
whileendbr = 0
whilefirstbr = 0
lastw = 0
wlistqnum = 0
inwlistq = 0
iflist = []
iffront = []
ifback = []
whilelistq = []
whilelistfront = []
whilelistback = []


print ("----------------------------------------------------")


def reject():
    print("REJECT")
    sys.exit(0)

def next():
    global i
    i += 1

def eat(*argv):
    for arg in argv:
        # print(arg)
        if token[i] == arg:
            next()
            return
        else:
            reject()

def program():
    dl()
    if token[i] == "$":
        return
    else:
        reject()


def dl():
    declaration()
    declarationprime()


def declarationprime():
    if token[i] == "int" or token[i] == "void":
        declaration()
        declarationprime()
    elif token[i] == "$":
        return
    else:
        return

def declaration():
    global q, currfunc
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha():
        next()
        funcparm = []
        if token[i-1] == "main":
            print (str(q).ljust(4) + "\tfunc \t\t" + token[i-1] + "\t\tvoid\t\t0")
            q += 1
            currfunc = token[i-1]

        else:
            if token[i-2] == "void":
                if token[i+1] == "void":
                    print (str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\tvoid\t\t0")
                    q += 1
                    currfunc = token[i-1]
                else:
                    f = i + 1
                    paramcount = 0
                    qch = q + 1
                    while token[f] != ")":
                        if token[f] == "int":
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f+1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print (str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print (v)
                    currfunc = token[i-1]

            else:
                if token[i+1] == "void":
                    print (str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t0")
                    q += 1
                    currfunc = token[i-1]
                else:
                    f = i + 1
                    paramcount = 0
                    qch = q + 1
                    while token[f] != ")":
                        if token[f] == "int":
                            paramcount += 1
                            funcparm.append(str(qch).ljust(4) + "\tparam\t\t4   \t\t\t\t\t" + token[f+1])
                            qch += 1
                            f += 2
                            if token[f] == ",":
                                f += 1
                    print (str(q).ljust(4) + "\tfunc \t\t" + token[i-1].ljust(4) + "\t\t" + token[i-2].ljust(4) + "\t\t" + str(paramcount))
                    q = qch
                    for v in funcparm:
                        print (v)
                    currfunc = token[i-1]

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
        elif token[i] == "(":
            next()
            params()
            if token[i] == ")":
                next()
                compoundstmt()
            else:
                reject()
        else:
            reject()
    else:
        reject()


def var_declaration():
    global q
    type_specifier()
    if token[i] not in wordarray and token[i].isalpha:
        next()
        if token[i] != "[":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1
            elif iniflist == 1:
                iflist.append(str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1
            else:
                print (str(q).ljust(4) + "\talloc\t\t4   \t\t    \t\t" + token[i-1])
                q += 1

    else:
        reject()
    if token[i] == ";":
        next()
    elif token[i] == "[":
        next()

        alloc = int(token[i]) * int(4)

        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1
        elif iniflist == 1:
            iflist.append(str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1
        else:
            print (str(q).ljust(4) + "\talloc\t\t" + str(alloc).ljust(4) + "\t\t    \t\t" + token[i-2])
            q += 1

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


def type_specifier():
    if token[i] == "int" or token[i] == "void":
        next()
    else:
        return

def params():
    if token[i] == "int" or token[i] == "void":
        paramslist()
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
    if token[i] not in wordarray and token[i].isalpha():
        next()
        if token[i] == "[":
            next()
            eat("]")
    else:
        if token[i-1] == "void":
            return
        else:
            reject()


def compoundstmt():
    global currfunc, q, incurrfun
    if token[i] == "{":
        next()
        incurrfun += 1

        if incurrfun > 1:
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            elif iniflist == 1:
                iflist.append(str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1
            else:
                print (str(q).ljust(4) + "\tblock\t\t    \t\t    ")
                q += 1

    else:
        return

    local_declaration()
    statementlist()

    if token[i] == "}":
        next()

        incurrfun -= 1
        if incurrfun > 0:
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            elif iniflist == 1:
                iflist.append(str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1
            else:
                print (str(q).ljust(4) + "\tend  \t\tblock\t\t")
                q += 1

        if incurrfun == 0:
            print (str(q).ljust(4) + "\tend  \t\tfunc\t\t" + currfunc)
            q += 1

    else:
        reject()


def local_declaration():
    ldprime()


def ldprime():
    if token[i] == "int" or token[i] == "void":
        var_declaration()
        ldprime()
    else:
        return


def statementlist():
    slprime()


def slprime():
    if token[i] not in wordarray and token[i].isalpha():
        statement()
        slprime()
    elif token[i].isnumeric():
        statement()
        slprime()
    elif token[i] == "(" or token[i] == ";" or token[i] == "{" or token[i] == "if" or token[i] == "while" or token[i] == "return":
        statement()
        slprime()
    elif token[i] == "}":
        return
    else:
        return


def statement():
    if token[i] not in wordarray and token[i].isalpha():
        expstmt()
    elif token[i].isnumeric():
        expstmt()
    elif token[i] == "(" or token[i] == ";":
        expstmt()
    elif token[i] == "{":
        compoundstmt()
    elif token[i] == "if":
        selectionstmt()
    elif token[i] == "while":
        itstmt()
    elif token[i] == "return":
        retstmt()
    else:
        reject()


def expstmt():
    if token[i] not in wordarray and token[i].isalpha():
        exp()
        eat(";")
    elif token[i].isnumeric:
        exp()
        eat(";")
    elif token[i] == "(":
        exp()
        eat(";")
    elif token[i] == ";":
        next()
    else:
        reject()


def selectionstmt():
    global ifbr, q, t, iniflist
    if token[i] == "if":
        next()
    else:
        return

    if token[i] == "(":
        next()
        f = i
        iffront = ""
        bch = 0
        while token[f] != "<" and token[f] != "<=" and token[f] != ">" and token[f] != ">=" and token[f] != "==" and token[f] != "!=":
            if token[f] == "[" or bch == 1:
                iffront = iffront + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                iffront = iffront + " " + token[f]
            f += 1


        comparison = token[f]
        iffront = infixToPostfix(iffront)
        lastif = postfixEval(iffront)

        f += 1
        bch = 0
        ifback = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                ifback = ifback + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                ifback = ifback + " " + token[f]
            f += 1

        ifback = infixToPostfix(ifback)
        lastif1 = postfixEval(ifback)

        print (str(q).ljust(4) + "\tcomp \t\t" + lastif.ljust(4) + "\t\t" + lastif1.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if comparison == ">":
            print (str(q).ljust(4) + "\tBRLEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == ">=":
            print (str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<":
            print (str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<=":
            print (str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "==":
            print (str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        else:  # comparison == "!="
            print (str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

        iflist.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        q += 1


    else:
        reject()

    exp()

    eat(")")

    iniflist = 1

    statement()

    if token[i] == "else":
        iflist[ifnum] = iflist[ifnum] + str(q+1)
    else:
        iflist[ifnum] = iflist[ifnum] + str(q)

    for v in iflist:
        print (v)
    iniflist = 0

    if token[i] == "else":
        next()

        iflist.append(str(q).ljust(4) + "\tBR   \t\t\t\t\t\t\t\t")
        elsech = len(iflist)
        q += 1
        iniflist = 1

        statement()

        iflist[elsech-1] = iflist[elsech-1] + str(q)

        for v in range(elsech-1, len(iflist)):
            print (iflist[v])
        iniflist = 0

    else:
        return


def itstmt():
    global lastw, t, q, inwlistq, dubcheck, wlistqnum
    if token[i] == "while":
        next()
    else:
        return

    if token[i] == "(":
        next()
        whileendbr = q
        f = i
        wlistfront = ""
        bch = 0
        while token[f] != "<" and token[f] != "<=" and token[f] != ">" and token[f] != ">=" and token[f] != "==" and token[f] != "!=":
            if token[f] == "[" or bch == 1:
                wlistfront = wlistfront + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                wlistfront = wlistfront + " " + token[f]
            f += 1

        comparison = token[f]
        wlistfront = infixToPostfix(wlistfront)
        lastw = postfixEval(wlistfront)

        f += 1
        bch = 0
        wlistback = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                wlistback = wlistback + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                wlistback = wlistback + " " + token[f]
            f += 1

        wlistback = infixToPostfix(wlistback)
        lastw1 = postfixEval(wlistback)

        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tcomp \t\t" + lastw.ljust(4) + "\t\t" + lastw1.ljust(4) + "\t\tt" + str(t))
        else:
            print (str(q).ljust(4) + "\tcomp \t\t" + lastw.ljust(4) + "\t\t" + lastw1.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1

        if comparison == ">":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBRLEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBRLEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == ">=":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBGET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBLT  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "<=":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBLET \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        elif comparison == "==":
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBEQ  \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1
        else:
            if inwlistq == 1:
                whilelistq.append(str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            else:
                print (str(q).ljust(4) + "\tBNEQ \t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(q + 2))
            q += 1

    else:
        reject()

    exp()
    eat(")")
    inwlistq = 1
    dubcheck += 1
    statement()
    dubcheck -= 1
    whilelistq[wlistqnum] = whilelistq[wlistqnum] + str(q + 1)  +"h"
    inwlistq = 0

    if dubcheck == 0:
        for v in whilelistq:
            print (v)

    if inwlistq == 1:
        whilelistq.append(str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileendbr))
    else:
        print (str(q).ljust(4) + "\tBR  \t\t\t\t\t\t\t\t" + str(whileendbr))
    q += 1


def retstmt():
    global q, t
    if token[i] == "return":
        next()
    else:
        return

    if token[i] == ";":
        next()
        print (str(q).ljust(4) + "\treturn\t\t    \t\t    ")
        q += 1
        return

    elif token[i] not in wordarray and token[i].isalpha():

        if token[i+1] == "[":
            f = i
            retexp = ""
            while token[f] != ";":
                retexp = retexp + token[f]
                f += 1

            h1 = retexp.partition('[')
            h2 = retexp.partition('[')[-1].rpartition(']')[0]
            if h2.isdigit() == False:
                print (str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                h2 = temp
            else:
                h2 = int(h2) * 4
            print (str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
            q += 1
            temp = "t" + str(t)
            t += 1

            print (str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + temp)
            q += 1

        else:
            print (str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[i])
            q += 1

        exp()

        eat(";")

    elif token[i].isnumeric():

        print (str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + token[i])
        q += 1

        exp()

        eat(";")
    elif token[i] == "(":

        f = i + 1
        bch = 0
        expret = ""
        while token[f] != ")":
            if token[f] == "[" or bch == 1:
                expret = expret + token[f]
                bch = 1
                if token[f] == "]":
                    bch = 0
            else:
                expret = expret + " " + token[f]
            f += 1

        expret = infixToPostfix(expret)
        lastexpret = postfixEval(expret)

        print (str(q).ljust(4) + "\treturn\t\t    \t\t    \t\t" + lastexpret)
        q += 1

        exp()

        eat(';')
    else:
        reject()


def exp():
    global i, q, t, inexp
    if token[i] not in wordarray and token[i].isalpha():
        next()

        if token[i] == "[" and inexp == 0:
            f = i - 1
            check = ""
            while token[f] != "=":
                check = check + token[f]
                f += 1
            i = f
            assign = check

            if inwlistq == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            elif iniflist == 1:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    iflist.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                iflist.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

            else:
                h1 = assign.partition('[')
                h2 = assign.partition('[')[-1].rpartition(']')[0]
                if h2.isdigit() == False:
                    print (str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    h2 = temp
                else:
                    h2 = int(h2) * 4
                print (str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                q += 1
                temp = "t" + str(t)
                t += 1
                assign = temp

        else:
            assign = token[i-1]

        if token[i] == "(" and inexp == 0:
            f = i
            exquad = token[i-1]
            while token[f] != ";":
                exquad = exquad + token[f]
                f += 1

            if inwlistq == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    whilelistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

            elif iniflist == 1:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    iflist.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                iflist.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

            else:
                parmcount = 0
                h1 = exquad.partition('(')[-1].rpartition(')')[0]
                h2 = exquad.partition('(')
                if ',' in h1:
                    h1 = h1.split(',')
                for v in h1:
                    parmcount += 1
                    print (str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                    q += 1

                print (str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                q += 1
                t += 1

        if token[i] == "=":
            f = i + 1
            exquad = ""
            bch = 0
            pch = 0
            while token[f] != ";":
                if token[f] == "[" or bch == 1:
                    exquad = exquad + token[f]
                    bch = 1
                    if token[f] == "]":
                        bch = 0
                elif token[f] == "(" or pch == 1:
                    if token[f-1] != "*" and token[f-1] != "/" and token[f-1] != "+" and token[f-1] != "-" and token[f-1] != "=":
                        exquad = exquad + token[f]
                        pch = 1
                        if token[f] == ")":
                            pch = 0
                    else:
                        exquad = exquad + " " + token[f]
                else:
                    exquad = exquad + " " + token[f]
                f += 1
            exquad = infixToPostfix(exquad)
            lastexp = postfixEval(exquad)

            if inwlistq == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        whilelistq.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    whilelistq.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    whilelistq.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    whilelistq.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

            elif iniflist == 1:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        iflist.append(str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    iflist.append(str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    iflist.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        iflist.append(str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    iflist.append(str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    iflist.append(str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    iflist.append(str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp =1

            else:
                if "(" in lastexp:
                    parmcount = 0
                    h1 = lastexp.partition('(')[-1].rpartition(')')[0]
                    h2 = lastexp.partition('(')
                    if ',' in h1:
                        h1 = h1.split(',')
                    for v in h1:
                        parmcount += 1
                        print (str(q).ljust(4) + "\targ  \t\t\t\t\t\t\t\t" + v)
                        q += 1

                    print (str(q).ljust(4) + "\tcall \t\t" + h2[0].ljust(4) + "\t\t" + str(parmcount).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1
                    print (str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp =1

                elif "[" in lastexp:
                    h1 = lastexp.partition('[')
                    h2 = lastexp.partition('[')[-1].rpartition(']')[0]
                    if h2.isdigit() == False:
                        print (str(q).ljust(4) + "\tmult \t\t" + h2.ljust(4) + "\t\t4   \t\tt" + str(t))
                        q += 1
                        temp = "t" + str(t)
                        t += 1
                        h2 = temp
                    else:
                        h2 = int(h2) * 4
                    print (str(q).ljust(4) + "\tdisp \t\t" + h1[0].ljust(4) + "\t\t" + str(h2).ljust(4) + "\t\tt" + str(t))
                    q += 1
                    temp = "t" + str(t)
                    t += 1

                    print (str(q).ljust(4) + "\tassgn\t\t" + temp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

                else:
                    print (str(q).ljust(4) + "\tassgn\t\t" + lastexp.ljust(4) + "\t\t\t\t\t" + str(assign))
                    q += 1
                    inexp = 1

        ex()
        inexp = 0

    elif token[i] == "(":
        next()
        exp()
        if token[i] == ")":
            next()
            termprime()
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            reject()
    elif token[i].isnumeric():
        next()
        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        elif token[i] == "+" or token[i] == "-":
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
        elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                         token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
        else:
            return
    else:
        reject()


def ex():
    if token[i] == "=":
        next()
        exp()
    elif token[i] == "[":
        next()
        exp()
        if token[i-1] == "[":
            reject()
        if token[i] == "]":
            next()
            if token[i] == "=":
                next()
                exp()
            elif token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
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
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            reject()
    elif token[i] == "*" or token[i] == "/":
        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "+" or token[i] == "-":
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                     token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


def var():
    if token[i] not in wordarray and token[i].isalpha():
        next()
    else:
        return
    if token[i] == "[":
        next()
        exp()
        eat("]")
    else:
        return


def simexp():
    addexp()
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


def relop():
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        next()
    else:
        return


def addexp():
    term()
    addexpprime()


def addexpprime():
    if token[i] == "+" or token[i] == "-":
        addop()
        term()
        addexpprime()
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
            exp()
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
        exp()
        if token[i] == ")":
            next()
        else:
            return
    else:
        reject()


def call():
    if token[i] not in wordarray and token[i].isalpha():
        next()
        if token[i] == "(":
            next()
            args()
            if token[i] == ")":
                next()
            else:
                reject()
        else:
            reject()
    else:
        return


def args():
    if token[i] not in wordarray and token[i].isalpha:
        arglist()
    elif token[i].isnumeric():
        arglist()
    elif token[i] == "(":
        arglist()
    elif token[i] == ")":
        return
    else:
        return


def arglist():
    exp()
    arglistprime()


def arglistprime():
    if token[i] == ",":
        next()
        exp()
        arglistprime()
    elif token[i] == ")":
        return
    else:
        return


def infixToPostfix(infixexpr):
    prec = {"*":3, "/":3, "+":2, "-":2, "(":1}
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) == True and "(" in token) or token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789" or token in "abcdefghijklmnopqrstuvwxyz":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

def postfixEval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token.isalnum() or "[" in token or ("(" in token and ")" in token) or (re.search('[a-z]', token) == True and "(" in token) or token.isalpha() or token.isnumeric():
            operandStack.push(token)
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = math(token,operand1,operand2)
            operandStack.push(result)
    return operandStack.pop()



def math(op, op1, op2):
    global q, t
    if op == "*":
        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        elif iniflist == 1:
            iflist.append(str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        else:
            print (str(q).ljust(4) + "\tmult \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    elif op == "/":
        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        elif iniflist == 1:
            iflist.append(str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        else:
            print (str(q).ljust(4) + "\tdiv  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    elif op == "+":
        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        elif iniflist == 1:
            iflist.append(str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        else:
            print (str(q).ljust(4) + "\tadd  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

    else:  # if op == "-"
        if inwlistq == 1:
            whilelistq.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        elif iniflist == 1:
            iflist.append(str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        else:
            print (str(q).ljust(4) + "\tsub  \t\t" + op1.ljust(4) + "\t\t" + op2.ljust(4) + "\t\tt" + str(t))
        q += 1
        temp = "t" + str(t)
        t += 1
        return temp

class Stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)

program()
print ("----------------------------------------------------")

