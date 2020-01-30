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
keywords = "[a-z]+"  # gets all words/ID's
numbers = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"  # gets all NUM's/float numbers
symbol = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # gets all special symbols
error = "\S"
comments = r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)'
#lexer
token = []
reading = file.read()
comment = re.sub(comments,"",reading)
for line in comment.split("\n"):
    regex = "(%s)|(%s)|(%s)|(%s)" % (keywords, numbers, symbol, error)
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
print (token)
