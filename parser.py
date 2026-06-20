from dataclasses import dataclass

@dataclass
class BinaryOp:
    left: any
    op: str
    right: any

@dataclass
class If:
    condition: any
    then_body: list
    else_body: list

@dataclass
class FuncDef:
    name: str
    params: list
    body: list

class Parser:
    def __init__(self, token):
        self.tokens = token
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype):
        tok = self.advance()
        if tok.type != ttype:
            raise ParseError(f"Expected {ttype}, got {tok.type} at line {tok.line}")
        return tok
