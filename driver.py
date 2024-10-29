import unittest
from typing import List, Dict, Any, Tuple
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator
from compiler import Compiler


'''For the sake of clarity, Please try and comment the code as you go.
    As much as possible'''






compiler = Compiler()
source_code = """
def test():
    print("Testing")
test()
x = 42
y = 21
z = x + y
print(x)
"""
success, result = compiler.compile(source_code)

tokens = Lexer.lexerFunc(Lexer(), source_code)
ast = Parser.parse(Parser(), tokens)
an_code = SemanticAnalyzer.analyze(SemanticAnalyzer(), ast)
IR = IRGenerator.generate(IRGenerator(), ast)
# print(ast)
print(IR)
