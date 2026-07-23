import os
import sys
import subprocess
import llvmlite.binding as llvm

from lexer import Lexer
from parser import Parser
from codegen import CodeGen

if len(sys.argv) <= 1:
    print("Usage: pyC <filename>.c")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as file:
    file_contents = file.read()

lexer = Lexer(file_contents)
tokens = lexer.tokenize()
tree = Parser(tokens).parse_program()
cg = CodeGen()
llvm_ir = cg.codegen(tree)

llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

mod = llvm.parse_assembly(llvm_ir)
mod.verify()

target_machine = llvm.Target.from_default_triple().create_target_machine()
obj_code = target_machine.emit_object(mod)

obj_path = "a.o"
exe_path = 'a'

with open(obj_path, "wb") as f:
    f.write(obj_code)

result = subprocess.run(["cc", obj_path, "-o", exe_path])
os.remove(obj_path)
if result.returncode != 0:
    print("Linking Failed!")
    sys.exit(1)

print(f"Built Executable: ./{exe_path}")