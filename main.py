import sys
from lexer import Lexer

if len(sys.argv) <= 1:
    print("Usgae: pyC <filename>.c");
    sys.exit(1);

filename = sys.argv[1]
file_contents = ''

with open(filename, 'r') as file:
    file_contents = file.read()

lexer = Lexer(file_contents)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type} {token.value} {token.line}")
