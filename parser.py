import ply.yacc as yacc
from lexer import Lexer

'''For the sake of clarity, Please try and comment the code as you go.
    As much as possible'''

lexer = Lexer()
parser = yacc.yacc(module=lexer)

