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
source_code = """
# Constants
number_of_students = 90
distance_in_meters = 1000  # Approximate distance between CIT lab and the stadium
average_stride_length = 0.78  # in meters

# Calculate steps per student
steps_per_student = distance_in_meters / average_stride_length

# Display result
print("The average number of steps required for each student to complete the walk is approximately:", steps_per_student)

"""
source_code = """
    x = 42
    print(x)
    """

# success, result = compiler.compile(source_code)

tokens = Lexer.lexerFunc(Lexer(), source_code)
ast = Parser.parse(Parser(), tokens)
# an_code = SemanticAnalyzer.analyze(SemanticAnalyzer(), ast)
IR = IRGenerator.generate(IRGenerator(), ast)
op_ir = Optimizer.optimize(Optimizer(), IR)
ass = CodeGenerator.generate(CodeGenerator(),op_ir)
print("=============================================")

# print(ast)
print(IR)
print("=============================================")
print(op_ir)
print("=============================================")
print(ass)
