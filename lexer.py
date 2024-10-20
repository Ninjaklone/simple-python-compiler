import re
from ply.lex import lex

'''For the sake of clarity, Please try and comment the code as you go.
    As much as possible'''
class Lexer:
    # List of token names
    tokens = (
        'NUMBER', 'STRING', 'COMMENT', 'NEWLINE', 'SKIP', 'KEYWORD', 
        'IDENT', 'OP', 'DELIM', 'L_PAREN', 'R_PAREN', 'EQUATE', 'TERMINAL'
    )

    # Regular expression rules for simple tokens
    t_NUMBER = r'\b\d+(\.\d*)?([eE][-+]?\d+)?\b'  # Integer or decimal number
    t_STRING = r'\".*?\"|\'.*?\''                  # String literals (single or double quotes)
    t_COMMENT = r'\#.*'                            # Comment
    t_NEWLINE = r'\n'                             # Line endings
    t_SKIP = r'[ \t]+'                            # Skip over spaces and tabs
    t_KEYWORD = r'\b(?:def|return|if|else|elif|for|while|break|continue|True|False|None)\b'  # "Reserved" words
    t_IDENT = r'[A-Za-z_][A-Za-z0-9_]*'          # Identifiers: Variables, Functions, etc.
    t_OP = r'[+\-*/%//==!=<>]=?|[@^&|~]'           # Operators: Arithmetic, Comparison, etc.
    t_DELIM = r'[(),:;{}[\].]'                     # Delimiters: You know the things that denote boundaries

    # Parentheses (Redundant but just cause we can)
    t_L_PAREN = r'\('  # Regex for left parenthesis
    t_R_PAREN = r'\)'  # Regex for right parenthesis
    t_EQUATE = r'='
    t_TERMINAL = r';'

    def __init__(self):
        # Create the lexer
        self.lexer = lex(module=self)

    def t_error(self, t):
        raise Exception(f"Illegal character '{t.value[0]}' at position {t.lexpos}")

    def lexerFunc(self, input_string):  # Tokenizer method
        # Input the string to the lexer
        self.lexer.input(input_string)
        tokens = []
        parentheses_count = 0  # Track parentheses balance

        # Iterate over the tokens and append them to the token list
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            if tok.type == 'NEWLINE':
                continue  # Skip newlines
            if tok.type == 'SKIP':
                continue  # Skip spaces and tabs
            tokens.append(tok.value)

            # Error Checking for Parentheses
            if tok.type == 'L_PAREN':
                parentheses_count += 1
            elif tok.type == 'R_PAREN':
                parentheses_count -= 1
                if parentheses_count < 0:
                    raise Exception("Unmatched closing parenthesis")

            # Error Checking for Unexpected Tokens
            if tok.type not in self.tokens:
                raise Exception(f"Unexpected token '{tok.value}' at position {tok.lexpos}")

        # Another Check just cause we can
        if parentheses_count != 0:
            raise Exception("Unmatched opening parenthesis")

        # Return the token list
        return tokens


