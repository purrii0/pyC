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
type → base_type '*'*
base_type → 'int'
          | 'char'
          | 'float'
          | 'void'
```
A type is a base type followed by zero or more `*`, one per level of
pointer indirection.

**Examples:**
```c
int x;        /* int          */
int *p;       /* pointer to int      */
int **pp;     /* pointer to pointer to int */
char *s;      /* pointer to char (a C string) */
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
float f = 3.14;
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
printf("x = %d\n", x);
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
      | '&' unary
      | '*' unary
      | primary
primary → INT_LIT
        | FLOAT_LIT
        | CHAR_LIT
        | STRING_LIT
        | IDENT
        | func_call
        | '(' expr ')'
```
`&expr` takes the address of `expr` (produces a pointer). `*expr`
dereferences a pointer (produces the value it points to). Both bind at the
same precedence as unary `-`, and are right-associative (`**p` dereferences
twice, `&&x` is not meaningful and should be rejected — see open issue below).

> **Note on grammar ambiguity:** `*` is now used for both *multiplication*
> (a binary operator, in `multiplication`) and *dereference* (a unary
> operator, in `unary`). The parser must disambiguate by position: `*`
> appearing where an operand is expected (start of a `unary`) is dereference;
> `*` appearing between two already-parsed operands is multiplication. This
> is the same ambiguity real C has, and real C parsers resolve it the same
> way — by parser position, not by a separate token.

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
printf("result: %d\n", x)
```

---

## Literals
```
INT_LIT    → [0-9]+
FLOAT_LIT  → [0-9]+ '.' [0-9]+
CHAR_LIT   → '\'' char '\''
STRING_LIT → '"' char* '"'
```
**Examples:**
```
42
3.14
'a'
"result: %d\n"
```
String literals support the standard escape sequences: `\n`, `\t`, `\\`, `\"`, `\0`.

---

## Identifiers and Keywords
```
IDENT → [a-zA-Z_][a-zA-Z0-9_]*
```
**Reserved keywords** (cannot be used as identifiers):
```
int   char   float   void   if   else   while   return
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

## Standard Library Functions

This subset recognizes a small, fixed set of C standard library functions as
callable without any `#include` or forward declaration in source. They are
parsed with ordinary `func_call` syntax; the compiler emits an LLVM `declare`
for each one automatically when it's used.

```
printf(STRING_LIT, arg_list?)   →  i32   (variadic — matches libc's printf)
scanf(STRING_LIT, arg_list?)    →  i32   (variadic — matches libc's scanf)
```

**Examples:**
```c
printf("fib(%d) = %d\n", n, result);

int x;
scanf("%d", &x);   /* &x takes x's address, so scanf can write into it */
```

---

## Comments
```
/* this is a block comment */
```
Single-line `//` comments are **not supported** in this subset.

---

## What is NOT supported
To keep scope small, the following are intentionally left out:
- Struct/array member and pointer-arithmetic access (`->`, `p[i]`, `p + 1`)
  — only single-value `&`/`*` (address-of / dereference) are supported,
  not pointer arithmetic or indexing
- Arrays
- Structs and enums
- `for` loops
- `switch` statements
- `do/while` loops
- Multiple assignment (`a = b = 0`)
- Preprocessor (`#include`, `#define`)
- `malloc` / `free`
- `//` single-line comments
- Standard library functions other than `printf`/`scanf`

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
    int n;
    printf("Enter n: ");
    scanf("%d", &n);

    int result = fib(n);
    printf("fib(%d) = %d\n", n, result);
    return 0;
}
```