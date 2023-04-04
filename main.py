from enum import Enum

# Define tokens as an enumeration
class Token(Enum):
    INTEGER = 1
    FLOAT = 2
    ID = 3
    BITWISE_OR = 4
    LOGICAL_OR = 5
    BITWISE_AND = 6
    LOGICAL_AND = 7
    FOR = 8
    WHILE = 9
    IF = 10
    ELSE = 11
    ERROR = 12

# Define a class for the return type of lex()
class LexResult:
    def __init__(self, token, index=None, int_value=None, float_value=None, string=None):
        self.token = token
        self.index = index
        self.int_value = int_value
        self.float_value = float_value
        self.string = string
    
    def __str__(self):
        result = "<token=" + self.token.name
        if self.index:
            result += ", index=" + str(self.index)
        if self.int_value:
            result += ", integer_value=" + str(self.int_value)
        if self.float_value:
            result += ", float_value=" + str(self.float_value)
        if self.string:
            result += ", unrecognized_string=" + self.string
        result += ">"
        return result

# Initialize symbol table with reserved words
symbol_table = {"for": Token.FOR, "while": Token.WHILE, "if": Token.IF, "else": Token.ELSE}

# Define lex() function to read input from file and return LexResult object
def lex(file_name):
    with open(file_name) as file:
        for line in file:
            for word in line.split():
                if word.isdigit(): # integer
                    yield LexResult(Token.INTEGER, int_value=int(word))
                elif is_float(word): # floating point number
                    yield LexResult(Token.FLOAT, float_value=float(word))
                elif is_identifier(word): # identifier
                    if word in symbol_table:
                        yield LexResult(symbol_table[word], index=0)
                    else:
                        index = len(symbol_table)
                        symbol_table[word] = Token.ID
                        yield LexResult(Token.ID, index=index)
                elif word == "|": # bitwise or
                    yield LexResult(Token.BITWISE_OR)
                elif word == "||": # logical or
                    yield LexResult(Token.LOGICAL_OR)
                elif word == "&": # bitwise and
                    yield LexResult(Token.BITWISE_AND)
                elif word == "&&": # logical and
                    yield LexResult(Token.LOGICAL_AND)
                else: # unrecognized lexeme
                    yield LexResult(Token.ERROR, string=word)

# Define helper function to check if a string is a floating point number
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Define helper function to check if a string is a valid identifier
def is_identifier(string):
    return string.isidentifier()

# Main program loop
while True:
    file_name = input("Enter input file name (or 'exit' to quit): ")
    if file_name == "exit":
        break
    print("Menu:")
    print("1. Call lex()")
    print("2. Show symbol table")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        for result in lex(file_name):
            print(result)
    elif choice == 2:
        print(symbol_table)
    elif choice == 3:
        break
    else:
        print("Invalid choice.")
