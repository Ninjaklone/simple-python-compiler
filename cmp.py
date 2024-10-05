import re, math
import ply, pyparsing, ast
from ply.lex import lex
from ply.lex import TOKEN

# steps = [1489, 1242, 1389, 1516, 1520, 1479, 1177, 1124, 1210, 1494, 1258, 1407, 1325, 
# 1270, 1432, 1192, 1327, 1349, 1120, 1175, 1193, 1196, 1506, 1473, 1268, 1235, 
# 1189, 1321, 1419, 1187, 1464, 1170, 1326, 1392, 1268, 1228, 1509, 1414, 1499, 
# 1137, 1467, 1284, 1262, 1122, 1221, 1236, 1248, 1168, 1305, 1326, 1159, 1270, 
# 1284, 1405, 1536, 1397, 1266, 1519, 1267, 1561, 1220, 1362, 1351, 1461, 1238, 
# 1432, 1129, 1561, 1319, 1496, 1136, 1402, 1157, 1189, 1485, 1263, 1133, 1169, 
# 1134, 1314, 1232, 1205, 1179, 1351, 1288, 1316, 1256, 1552, 1498, 1254]

#The




#TOKENIZER

def lexerFunc(input_string):  #Tokenizer, whitespace ignored, Simple Error Detection, Token Stream Generation
    # Initial implementation using re.findall
    # token = re.findall(r"[\w]+|[\[\],]", input_string)
    # return token

    # Re-implementation using the ply library
    

    # Define the tokens
    tokens = ('WORD', 'LBRACKET', 'RBRACKET', 'COMMA', 'WHITESPACE', 'IDENTIFIER', 'NUMBER', 'STRING', 'COMMENT',
               'PARENTHESES', 'EQUATE', 'TERMINAL')

    # Token Definitions
    t_WORD = r'\w+'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUMBER = r'\d+(\.\d+)?'
    t_STRING = r'\".*?\"'
    t_COMMENT = r'\#.*'
    t_WHITESPACE = r'\s+'  # This will be ignored
    t_PARENTHESES = r'[()]'
    t_EQUATE = r'[=\+]'
    t_TERMINAL = r'[;]'

    # Error handling rule
    def t_error(t):
        raise Exception(f"Illegal character '{t.value[0]}'")

    # Create the lexer
    lexer = lex()
    # Input the string to the lexer
    lexer.input(input_string)
    # Initialize the token list
    token = []
    # Iterate over the tokens and append them to the token list
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type != 'WHITESPACE': #Ignores whitespaces
            token.append(tok.value)
    # Return the token list
    return token



#PARSER

def parser():
    return




#CODE GENERATOR




#DRIVER




#TEST CASE

# input_code = """    if(i==j)
#         z=0;
#     else
#         z=1;"""

input_code = """avg[x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49
 , x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66
 , x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83
 , x84, x85, x86, x87, x88, x89, x90]"""

dis = {
    'x1': 1489, 'x2': 1242, 'x3': 1389, 'x4': 1516, 'x5': 1520, 'x6': 1479, 'x7': 1177, 'x8': 1124, 'x9': 1210, 'x10': 1494,
    'x11': 1258, 'x12': 1407, 'x13': 1325, 'x14': 1270, 'x15': 1432, 'x16': 1192, 'x17': 1327, 'x18': 1349, 'x19': 1120, 'x20': 1175,
    'x21': 1193, 'x22': 1196, 'x23': 1506, 'x24': 1473, 'x25': 1268, 'x26': 1235, 'x27': 1189, 'x28': 1321, 'x29': 1419, 'x30': 1187,
    'x31': 1464, 'x32': 1170, 'x33': 1326, 'x34': 1392, 'x35': 1268, 'x36': 1228, 'x37': 1509, 'x38': 1414, 'x39': 1499, 'x40': 1137,
    'x41': 1467, 'x42': 1284, 'x43': 1262, 'x44': 1122, 'x45': 1221, 'x46': 1236, 'x47': 1248, 'x48': 1168, 'x49': 1305, 'x50': 1326,
    'x51': 1159, 'x52': 1270, 'x53': 1284, 'x54': 1405, 'x55': 1536, 'x56': 1397, 'x57': 1266, 'x58': 1519, 'x59': 1267, 'x60': 1561,
    'x61': 1220, 'x62': 1362, 'x63': 1351, 'x64': 1461, 'x65': 1238, 'x66': 1432, 'x67': 1129, 'x68': 1561, 'x69': 1319, 'x70': 1496,
    'x71': 1136, 'x72': 1402, 'x73': 1157, 'x74': 1189, 'x75': 1485, 'x76': 1263, 'x77': 1133, 'x78': 1169, 'x79': 1134, 'x80': 1314,
    'x81': 1232, 'x82': 1205, 'x83': 1179, 'x84': 1351, 'x85': 1288, 'x86': 1316, 'x87': 1256, 'x88': 1552, 'x89': 1498, 'x90': 1254
}

print(lexerFunc(input_code))
