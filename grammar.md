# C Grammar Reference

This file defines the grammar of the C subset this compiler supports.
It uses **BNF-style notation** — read it top to bottom, each rule defines what something is made of.

```
A → B C     means "A is made of B followed by C"
A → B | C   means "A is either B or C"
A → B*      means "zero or more B"
A → B?      means "B is optional"
```

---

## Program

```
program → function_def*
```

A program is zero or more function definitions.

---

## Function Definition

```
function_def → type IDENT '(' param_list ')' block

param_list → ε
           | param (',' param)*

param → type IDENT
```

**Example:**
```c
int add(int x, int y) {
    return x + y;
}
```

---

## Types

```
type → 'int'
     | 'char'
     | 'void'
```

---

## Block and Statements

```
block → '{' statement* '}'

statement → var_decl
          | assign_stmt
          | return_stmt
          | if_stmt
          | while_stmt
          | expr_stmt
```

---

### Variable Declaration

```
var_decl → type IDENT ('=' expr)? ';'
```

**Examples:**
```c
int x;
int y = 10;
char c = 'a';
```

---

### Assignment

```
assign_stmt → IDENT '=' expr ';'
```

**Example:**
```c
x = x + 1;
```

---

### Return

```
return_stmt → 'return' expr ';'
```

**Example:**
```c
return x + y;
```

---

### If / Else

```
if_stmt → 'if' '(' expr ')' block ('else' block)?
```

**Examples:**
```c
if (x > 0) {
    return x;
}

if (x > 0) {
    return x;
} else {
    return 0;
}
```

---

### While

```
while_stmt → 'while' '(' expr ')' block
```

**Example:**
```c
while (x > 0) {
    x = x - 1;
}
```

---

### Expression Statement

```
expr_stmt → func_call ';'
```

A bare function call used as a statement (return value discarded).

**Example:**
```c
print(x);
```

---

## Expressions

Expressions are listed from **lowest to highest precedence**.
Higher precedence means the operator binds tighter — `*` before `+`, for example.

```
expr → comparison

comparison → addition (('==' | '!=' | '<' | '>' | '<=' | '>=') addition)*

addition → multiplication (('+' | '-') multiplication)*

multiplication → unary (('*' | '/') unary)*

unary → '-' unary
      | primary

primary → INT_LIT
        | FLOAT_LIT
        | CHAR_LIT
        | IDENT
        | func_call
        | '(' expr ')'
```

---

### Function Call

```
func_call → IDENT '(' arg_list ')'

arg_list → ε
         | expr (',' expr)*
```

**Examples:**
```c
fib(10)
add(x, y + 1)
```

---

## Literals

```
INT_LIT   → [0-9]+
FLOAT_LIT → [0-9]+ '.' [0-9]+
CHAR_LIT  → '\'' char '\''
```

**Examples:**
```
42
3.14
'a'
```

---

## Identifiers and Keywords

```
IDENT → [a-zA-Z_][a-zA-Z0-9_]*
```

**Reserved keywords** (cannot be used as identifiers):

```
int   char   void   if   else   while   return
```

---

## Operators

| Operator | Meaning | Precedence |
|---|---|---|
| `==` `!=` `<` `>` `<=` `>=` | comparison | lowest |
| `+` `-` | addition / subtraction | |
| `*` `/` | multiplication / division | |
| `-` (unary) | negation | |
| `( )` | grouping | highest |

---

## Comments

```
/* this is a block comment */
```

Single-line `//` comments are **not supported** in this subset.

---

## What is NOT supported

To keep scope small, the following are intentionally left out:

- Pointers (`*`, `&`, `->`)
- Arrays
- Structs and enums
- `for` loops
- `switch` statements
- `do/while` loops
- Multiple assignment (`a = b = 0`)
- Preprocessor (`#include`, `#define`)
- `malloc` / `free`
- `//` single-line comments

---

## Full Example

A complete program this compiler can handle:

```c
int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    return fib(10);
}
```