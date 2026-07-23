from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INT_LIT = auto()
    FLOAT_LIT = auto()
    CHAR_LIT = auto()
    KEYWORD = auto()
    IDENT = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    GT = auto()
    LT = auto()
    EQ = auto()
    NQ = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMI = auto()
    ASSIGN = auto()
    GTE = auto()
    LTE = auto()
    EOF = auto()


@dataclass()
class Token:
    type: TokenType
    val: str
    line: int


keywords = {'char', 'int', 'void', 'float', 'if', 'else', 'while', 'return'}


class LexError(Exception):
    pass


class Lexer:
    def __init__(self, src):
        self.src = src
        self.line = 1
        self.pos = 0

    def peek(self):
        if self.pos < len(self.src):
            return self.src[self.pos]
        else:
            return ''

    def advance(self):
        ch = self.src[self.pos]
        self.pos += 1
        return ch

    def skip_whitespaces(self):
        while self.peek() in (' ', '\t', '\r', '\n'):
            if self.peek() == '\n':
                self.line += 1
            self.advance()

    def next_token(self):
        self.skip_whitespaces()
        ch = self.advance()
        if ch == '+': return Token(TokenType.PLUS, '+', self.line)
        if ch == '-': return Token(TokenType.MINUS, '-', self.line)
        if ch == '*': return Token(TokenType.MULTIPLY, '*', self.line)
        if ch == '/':
            if self.peek() == '*':
                self.skip_block_comment()
                return None
            return Token(TokenType.DIVIDE, '/', self.line)
        if ch == ';': return Token(TokenType.SEMI, ';', self.line)
        if ch == ',': return Token(TokenType.COMMA, ',', self.line)
        if ch == '(': return Token(TokenType.LPAREN, '(', self.line)
        if ch == ')': return Token(TokenType.RPAREN, ')', self.line)
        if ch == '{': return Token(TokenType.LBRACE, '{', self.line)
        if ch == '}': return Token(TokenType.RBRACE, '}', self.line)
        if ch in ('=', '!', '<', '>'):
            return self.read_two_char(ch)
        if ch.isdigit():
            return self.read_number(ch)
        if ch.isalpha() or ch == '_':
            return self.read_ident(ch)
        raise LexError(f"Unknown character '{ch}' at line {self.line}")

    def read_two_char(self, ch):
        if ch == '=':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.EQ, '==', self.line)
            return Token(TokenType.ASSIGN, '=', self.line)
        if ch == '!':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.NQ, '!=', self.line)
            raise LexError(f"Unknown character '{ch}' at line {self.line}")
        if ch == '<':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.LTE, '<=', self.line)
            return Token(TokenType.LT, '<', self.line)
        if ch == '>':
            if self.peek() == '=':
                self.advance()
                return Token(TokenType.GTE, '>=', self.line)
            return Token(TokenType.GT, '>', self.line)
        raise LexError(f"Unknown character '{ch}' at line {self.line}")

    def read_ident(self, first_ch):
        word = first_ch
        while self.peek().isalnum() or self.peek() == '_':
            word += self.advance()
        ttype = TokenType.KEYWORD if word in keywords else TokenType.IDENT
        return Token(ttype, word, self.line)

    def read_number(self, first_ch):
        num = first_ch
        while self.peek().isdigit():
            num += self.advance()
        if self.peek() == '.':
            num += self.advance()
            while self.peek().isdigit():
                num += self.advance()
            return Token(TokenType.FLOAT_LIT, num, self.line)
        return Token(TokenType.INT_LIT, num, self.line)

    def skip_block_comment(self):
        self.advance()
        while True:
            ch = self.advance()
            if ch == '*' and self.peek() == '/':
                self.advance()
                return
            if ch == '\n':
                self.line += 1

    def tokenize(self):
        tokens = []
        while self.pos < len(self.src):
            token = self.next_token()
            if token: tokens.append(token)
        tokens.append(Token(TokenType.EOF, '', self.line))
        return tokens
