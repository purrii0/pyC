import random
from dataclasses import dataclass
from mimetypes import add_type
from multiprocessing import context
from time import sleep
from typing import Any
from unittest import expectedFailure
from urllib import parse

from lexer import TokenType, Token

@dataclass
class Program:
    function: list
@dataclass
class BinaryOp:
    left: Any
    op: str
    right: Any
@dataclass
class UnaryOp:
    op: str
    expr: Any
@dataclass
class If:
    condition: Any
    then_body: list
    else_body: list
@dataclass
class FuncDef:
    type: str
    name: str
    params: list
    body: list
@dataclass
class IntLiteral:
    value: Any
@dataclass
class CharLiteral:
    value: Any
@dataclass
class FloatLiteral:
    value: Any
@dataclass
class Identifier:
    name: str
@dataclass
class Assign:
    name: str
    value: Any
@dataclass
class Return:
    expr: Any
@dataclass
class While:
    condition: Any
    body: list
@dataclass
class FuncCall:
    name: str
    args: list
@dataclass
class VarDecl:
    type: str
    name: str
    init: Any

class ParseError(Exception):
    pass
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def peekAhead(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype):
        tok = self.advance()
        if tok.type != ttype:
            raise ParseError(f"Expected {ttype}, got {tok.type} at line {tok.line}")
        return tok

    def parse_program(self):
        funcList = []
        while self.peek().type != TokenType.EOF:
            res = self.parse_function()
            funcList.append(res)
        return Program(funcList)

    def parse_function(self):
        return_type = self.expect(TokenType.KEYWORD)
        func_name = self.expect(TokenType.IDENT)
        self.expect(TokenType.LPAREN)
        params = self.parse_params()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FuncDef(return_type.val, func_name.val, params, body)
    def parse_params(self):
        params = []
        if self.peek().type == TokenType.RPAREN:
            return params
        token_type = self.expect(TokenType.KEYWORD)
        token_name = self.expect(TokenType.IDENT)
        params.append((token_type.val, token_name.val))
        while self.peek().type == TokenType.COMMA:
            self.advance()
            token_type = self.expect(TokenType.KEYWORD)
            token_name = self.expect(TokenType.IDENT)
            params.append((token_type.val, token_name.val))
        return params
    def parse_block(self):
        self.expect(TokenType.LBRACE)
        stmts = []
        while self.peek().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            stmts.append(stmt)
        return stmts

    def parse_statement(self):
        tok = self.peek()
        if tok.type == TokenType.KEYWORD:
            if tok.val in ('int', 'char', 'void', 'float'):
                return self.parse_var_decl()
            elif tok.val == 'if':
                return self.parse_if()
            elif tok.val == 'while':
                return self.parse_while()
            elif tok.val == 'return':
                return self.parse_return()
        elif tok.type == TokenType.IDENT:
            if self.peekAhead().type == TokenType.ASSIGN:
                return self.parse_assign()
            elif self.peekAhead().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                raise ParseError("unexpected token after identifier")
        else:
            raise ParseError(f"unexpected token {tok.type} at start of statement")
    def parse_var_decl(self):
        token_type = self.expect(TokenType.KEYWORD)
        token_name = self.expect(TokenType.IDENT)

        if self.peek().type == TokenType.ASSIGN:
            self.advance()
            init = self.parse_expression()
        else:
            init = None
        self.expect(TokenType.SEMI)
        return VarDecl(token_type.val, token_name.val, init)
    def parse_function_call(self):
        pass
    def parse_assign(self):
        pass
    def parse_if(self):
        pass
    def parse_while(self):
        pass
    def parse_return(self):
        pass
    def parse_expression(self):
        pass
    def parse_additive(self):
        pass
    def parse_term(self):
        pass
    def parse_unary(self):
        pass
    def parse_primary(self):
        pass