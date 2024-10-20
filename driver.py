import unittest
from lexer import Lexer  # Assuming the lexer class is in lexer.py





# input_code = '''steps = [1489, 1242, 1389, 1516, 1520, 1479, 1177, 1124, 1210, 1494, 1258, 1407, 1325, 
# 1270, 1432, 1192, 1327, 1349, 1120, 1175, 1193, 1196, 1506, 1473, 1268, 1235, 
# 1189, 1321, 1419, 1187, 1464, 1170, 1326, 1392, 1268, 1228, 1509, 1414, 1499, 
# 1137, 1467, 1284, 1262, 1122, 1221, 1236, 1248, 1168, 1305, 1326, 1159, 1270, 
# 1284, 1405, 1536, 1397, 1266, 1519, 1267, 1561, 1220, 1362, 1351, 1461, 1238, 
# 1432, 1129, 1561, 1319, 1496, 1136, 1402, 1157, 1189, 1485, 1263, 1133, 1169, 
# 1134, 1314, 1232, 1205, 1179, 1351, 1288, 1316, 1256, 1552, 1498, 1254]'''

# print(Lexer.lexerFunc(Lexer(),input_code))

# class TestLexer(unittest.TestCase):
#     def setUp(self):
#         self.lexer = Lexer()

#     def test_tokenization(self):
#         input_code = """if(i==j)
#                         z=0;
#                         else
#                         z=1;"""
#         expected_tokens = ['if', '(', 'i', '==', 'j', ')', 'z', '=', '0', ';', 'else', 'z', '=', '1', ';']
#         actual_tokens = self.lexer.lexerFunc(input_code)
#         self.assertEqual(actual_tokens, expected_tokens)

# if __name__ == '__main__':
#     unittest.main()


input_code = """class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def test_tokenization(self):
        expected_tokens = ['if', '(', 'i', '==', 'j', ')', 'z', '=', '0', ';', 'else', 'z', '=', '1', ';']
        actual_tokens = self.lexer.lexerFunc(input_code)
        self.assertEqual(actual_tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()"""

print(Lexer.lexerFunc(Lexer(),input_code))