from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    KEYWORD = 1
    IDENT = 2
    INT_LIT = 3
    FLOAT_LIT = 4
    STRING_LIT = 5
    PLUS = 6
    MINUS = 7
    STAR = 8
    SLASH = 9
    EQ = 10
    NEQ = 11
    LT = 12
    GT = 13
    ASSIGN = 14
    LPAREN = 15
    RPAREN = 16
    LBRACE = 17
    RBRACE = 18
    SEMI = 19
    COMMA = 20
    EOF = 21

KEYWORDS = {'if', 'else', 'while', 'return', 'int', 'float', 'string'}

@dataclass
class Token:
    type: TokenType
    value: str
    line: int

class Lexer:
    def __init__(self, source):
        self.src = source
        self.pos = 0
        self.line = 1

    def peek(self):
        return self.src[self.pos] if self.pos < len(self.src) else ''

    def advance(self):
        ch = self.src[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.src) and self.src[self.pos].isspace():
            if self.src[self.pos] == '\n':
                self.line += 1
            self.pos += 1

    def match(self, expected):
        if self.pos < len(self.src) and self.src[self.pos] == expected:
            self.pos += 1
            return True
        return False

    def read_string(self):
        result = []

        while self.pos < len(self.src) and self.src[self.pos] != '"':
            ch = self.advance()
            if ch == '\\' and self.peek() in ('"', '\\', 't', 'n'):
                result.append('\\' + self.advance())
            else:
                result.append(ch)
        if self.pos > len(self.src):
            raise SyntaxError(f"Unterminated string on line {self.line}")

        self.pos += 1
        return ''.join(result)

    def next_token(self):
        self.skip_whitespace()

        if self.pos >= len(self.src):
            return Token(TokenType.EOF, '', self.line)

        line = self.line
        ch = self.advance()

        if ch == '+': return Token(TokenType.PLUS,   '+', line)
        if ch == '-': return Token(TokenType.MINUS,  '-', line)
        if ch == '*': return Token(TokenType.STAR,   '*', line)
        if ch == '/': return Token(TokenType.SLASH,  '/', line)
        if ch == '(': return Token(TokenType.LPAREN, '(', line)
        if ch == ')': return Token(TokenType.RPAREN, ')', line)
        if ch == '{': return Token(TokenType.LBRACE, '{', line)
        if ch == '}': return Token(TokenType.RBRACE, '}', line)
        if ch == ';': return Token(TokenType.SEMI,   ';', line)
        if ch == ',': return Token(TokenType.COMMA,  ',', line)

        if ch == '=':
            if self.match('='):
                return Token(TokenType.EQ, '==', line)
            else:
                return Token(TokenType.ASSIGN, '=', line)
        if ch == '!':
            if self.match('='):
                return Token(TokenType.NEQ, '!=', line)
            raise SyntaxError(f"Unexpected '!' on line {line}")

        if ch == '<':
            if self.match('='):
                return Token(TokenType.EQ, '<=', line)
            return Token(TokenType.LT,      '<', line)

        if ch == '>':
            if self.match('='):
                return Token(TokenType.EQ, '>=', line)
            return Token(TokenType.GT,      '>', line)

        if ch == '"':
            value = self.read_string()
            return Token(TokenType.STRING_LIT, value, line)

        if ch.isdigit():
            digits = [ch]
            while self.peek().isdigit():
                digits.append(self.advance())
            if self.peek() == '.' and self.pos + 1 < len(self.src) and self.src[self.pos + 1].isdigit():
                digits.append(self.advance())
                while self.peek().isdigit():
                    digits.append(self.advance())
                return Token(TokenType.FLOAT_LIT, ''.join(digits), line)
            return Token(TokenType.INT_LIT, ''.join(digits), line)

        if ch.isalpha() or ch == '_':
            name = [ch]
            while self.peek().isalnum() or self.peek() == '_':
                name.append(self.advance())
            text = ''.join(name)
            tok_type = TokenType.KEYWORD if text in KEYWORDS else TokenType.IDENT
            return Token(tok_type, text, line)

        raise SyntaxError(f"Unexpected character {ch!r} on line {line}")

    def tokenize(self):
        tokens = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens
