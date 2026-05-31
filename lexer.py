from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    KEYWORD    = auto()
    IDENT      = auto()
    INT_LIT    = auto()
    FLOAT_LIT  = auto()
    STRING_LIT = auto()
    CHAR_LIT   = auto()
    PLUS       = auto()
    MINUS      = auto()
    STAR       = auto()
    SLASH      = auto()
    EQ         = auto()
    NEQ        = auto()
    LT         = auto()
    GT         = auto()
    LTE        = auto()
    GTE        = auto()
    ASSIGN     = auto()
    LPAREN     = auto()
    RPAREN     = auto()
    LBRACE     = auto()
    RBRACE     = auto()
    SEMI       = auto()
    COMMA      = auto()
    EOF        = auto()

KEYWORDS = {'if', 'else', 'while', 'return', 'int', 'float', 'char'}

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
            self.pos +=

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
        if self.pos >= len(self.src):
            raise SyntaxError(f"Unterminated string on line {self.line}")

        self.pos += 1
        return ''.join(result)

    def read_char(self):
        if self.pos >= len(self.src):
            raise SyntaxError(f"Unterminated char literal on line {self.line}")

        ch = self.advance()

        if ch == '\\':
            if self.peek() not in ('\'', '\\', 'n', 't', 'r', '0'):
                raise SyntaxError(f"Unknown escape in char literal on line {self.line}")
            ch = '\\' + self.advance()

        if self.pos >= len(self.src) or self.src[self.pos] != "'":
            raise SyntaxError(f"Char literal not closed on line {self.line}")


        self.pos += 1
        return ch

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
                return Token(TokenType.LTE, '<=', line)
            return Token(TokenType.LT,      '<', line)

        if ch == '>':
            if self.match('='):
                return Token(TokenType.GTE, '>=', line)
            return Token(TokenType.GT,      '>', line)

        if ch == '"':
            value = self.read_string()
            return Token(TokenType.STRING_LIT, value, line)

        if ch == "'":
            value = self.read_char()
            return Token(TokenType.CHAR_LIT, value, line)

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
