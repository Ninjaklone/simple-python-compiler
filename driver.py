import unittest
from lexer import Lexer  # Assuming the lexer class is in lexer.py

'''For the sake of clarity, Please try and comment the code as you go.
    As much as possible'''

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


input_code = open('note.txt','r').read()

print(Lexer.lexerFunc(Lexer(),input_code))