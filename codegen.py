from parser import (
    Program, BinaryOp, UnaryOp, If, FuncDef, IntLiteral, CharLiteral,
    FloatLiteral, Identifier, Assign, Return, While, FuncCall, VarDecl
)


class CodeGenError(Exception):
    pass

instructions = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "sdiv",
    "<": "icmp slt",
    ">": "icmp sgt",
    "<=": "icmp sle",
    ">=": "icmp sge",
    "==": "icmp eq",
    "!=": "icmp ne"
}


class CodeGen:
    def __init__(self):
        self.lines = []
        self.reg_count = 0
        self.symtab = {}

    def new_reg(self):
        self.reg_count += 1
        return f"%{self.reg_count}"

    def emit(self, line):
        self.lines.append(f"    {line}")

    def emit_header(self, line):
        self.lines.append(line)

    def gen_expr(self, node):
        if isinstance(node, IntLiteral):
            return node.value
        elif isinstance(node, Identifier):
            reg_ptr = self.symtab[node.name]
            reg = self.new_reg()
            self.emit(f"{reg} = load i32, ptr {reg_ptr}, align 4")
            return reg
        elif isinstance(node, BinaryOp):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            reg = self.new_reg()
            instr = instructions[node.op]
            self.emit(f"{reg} = {instr} i32 {left}, {right}")
            return reg
        elif isinstance(node, UnaryOp):
            value = self.gen_expr(node.expr)
            reg = self.new_reg()
            self.emit(f"{reg} = sub i32 0, {value}")
            return reg
        elif isinstance(node, FuncCall):
            return self.gen_func_call(node)

    def gen_stmt(self, node):
        if isinstance(node, VarDecl):
            reg = self.new_reg()
            self.symtab[node.name] = reg
            self.emit(f"{reg} = alloca i32, align 4")
            if node.init is not None:
                value = self.gen_expr(node.init)
                self.emit(f"store i32 {value}, ptr {reg}, align 4")
        elif isinstance(node, Assign):
            value = self.gen_expr(node.value)
            reg_ptr = self.symtab[node.name]
            self.emit(f"store i32 {value}, ptr {reg_ptr}, align 4")
        elif isinstance(node, Return):
            if self.current_ret_type == 'void':
                self.emit("ret void")
            else:
                value = self.gen_expr(node.expr)
                self.emit(f"ret i32 {value}")
        elif isinstance(node, If):
            self.gen_if(node)
        elif isinstance(node, While):
            self.gen_while(node)
        elif isinstance(node, FuncCall):
            self.gen_expr(node)

    def gen_function(self, node):
        self.lines = []
        self.reg_count = len(node.params)
        self.symtab = {}
        self.current_ret_type = node.type

        params_list = ", ".join(f"i32 %{i}" for i in range(len(node.params)))
        self.emit_header(f"define {'void' if self.current_ret_type == 'void' else 'i32'} @{node.name}({params_list}) {{")

        for i, (ptype, pname) in enumerate(node.params):
            reg = self.new_reg()
            self.emit(f"{reg} = alloca i32, align 4")
            self.emit(f"store i32 %{i}, ptr {reg}, align 4")
            self.symtab[pname] = reg

        for stmt in node.body:
            self.gen_stmt(stmt)

        self.emit_header("}")
        return '\n'.join(self.lines)

    def gen_if(self, node):
        cond_reg = self.gen_expr(node.condition)

        then_label = f"then{self.new_reg()[1:]}"
        else_label = f"else{self.new_reg()[1:]}"
        end_label  = f"end{self.new_reg()[1:]}"

        self.emit(f"br i1 {cond_reg}, label %{then_label}, label %{else_label}")
        self.emit_header(f"{then_label}:")

        for stmt in node.then_body:
            self.gen_stmt(stmt)
        if not (node.then_body and isinstance(node.then_body[-1], Return)):
            self.emit(f"br label %{end_label}")

        self.emit_header(f"{else_label}:")
        for stmt in node.else_body:
            self.gen_stmt(stmt)
        if not (node.else_body and isinstance(node.else_body[-1], Return)):
            self.emit(f"br label %{end_label}")

        self.emit_header(f"{end_label}:")

    def gen_while(self, node):
        body_label = f"word{self.new_reg()[1:]}"
        cond_label = f"word{self.new_reg()[1:]}"
        end_label = f"word{self.new_reg()[1:]}"

        self.emit(f"br label %{cond_label}")

        self.emit_header(f"{cond_label}:")
        cond_reg = self.gen_expr(node.condition)
        self.emit(f"br i1 {cond_reg}, label %{body_label}, label %{end_label}")

        self.emit_header(f"{body_label}:")
        for stmt in node.body:
            self.gen_stmt(stmt)
        if not (node.body and isinstance(node.body[-1], Return)):
            self.emit(f"br label %{cond_label}")

        self.emit_header(f"{end_label}:")

    def gen_func_call(self, node):
        args_vals = []
        for arg in node.args:
            args_vals.append(self.gen_expr(arg))
        args_text = ', '.join(f"i32 {v}" for v in args_vals)
        reg = self.new_reg()
        self.emit(f"{reg} = call i32 @{node.name}({args_text})")
        return reg