import sys
from lexer import Lexer

if len(sys.argv) <= 1:
    print("Usage: pyC <filename>.c")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as file:
    file_contents = file.read()

lexer = Lexer(file_contents)
tokens = lexer.tokenize()
