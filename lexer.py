import re
from ply.lex import lex

'''For the sake of clarity, Please try and comment the code as you go.
    As much as possible'''
class Lexer:
    # List of token names - Added more specific token types
    tokens = (
        'NUMBER_INT', 'NUMBER_FLOAT', 'STRING', 'COMMENT', 'NEWLINE', 'SKIP',
        'KEYWORD', 'IDENT', 'OP_ARITH', 'OP_COMP', 'OP_LOGIC', 'OP_BITWISE',
        'DELIM', 'L_PAREN', 'R_PAREN', 'L_BRACE', 'R_BRACE', 'L_BRACKET', 'R_BRACKET',
        'ASSIGN', 'COMMA', 'DOT', 'COLON', 'SEMICOLON'
    )

    # More comprehensive keyword list
    keywords = {
        'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
        'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
        'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
        'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        'True', 'False', 'None'
    }

    # Regular expression rules with better precision
    t_NUMBER_INT = r'\b\d+\b'
    t_NUMBER_FLOAT = r'\b\d*\.\d+([eE][-+]?\d+)?\b|\b\d+\.\d*([eE][-+]?\d+)?\b|\b\d+[eE][-+]?\d+\b'
    t_STRING = r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'  # Handles escaped quotes
    t_COMMENT = r'\#[^\n]*'
    t_NEWLINE = r'[\n]+'
    t_SKIP = r'[ \t]+'
    
    # Split operators by type
    t_OP_ARITH = r'[+\-*/%]|//|\*\*'
    t_OP_COMP = r'==|!=|<=|>=|<|>'
    t_OP_LOGIC = r'and|or|not'
    t_OP_BITWISE = r'&|\||\^|~|<<|>>'
    
    # More specific delimiters
    t_L_PAREN = r'\('
    t_R_PAREN = r'\)'
    t_L_BRACE = r'\{'
    t_R_BRACE = r'\}'
    t_L_BRACKET = r'\['
    t_R_BRACKET = r'\]'
    t_ASSIGN = r'=|\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|>>=|<<='
    t_COMMA = r','
    t_DOT = r'\.'
    t_COLON = r':'
    t_SEMICOLON = r';'

    def t_IDENT(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        # Check if identifier is a keyword
        t.type = 'KEYWORD' if t.value in self.keywords else 'IDENT'
        return t

    def t_error(self, t):
        raise Exception(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")

    def __init__(self):
        # Initialize line counting
        self.lexer = lex(module=self, reflags=re.UNICODE)
        self.line_number = 1

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def lexerFunc(self, input_string):
        self.lexer.input(input_string)
        tokens = []
        errors = []
        
        # Stack for tracking balanced delimiters
        delim_stack = []
        delim_pairs = {
            'L_PAREN': ('R_PAREN', '()'),
            'L_BRACE': ('R_BRACE', '{}'),
            'L_BRACKET': ('R_BRACKET', '[]')
        }

        while True:
            try:
                tok = self.lexer.token()
                if not tok:
                    break
                
                # Skip only whitespace, keep newlines and comments
                if tok.type == 'SKIP':
                    continue

                # Track delimiter balance
                if tok.type in delim_pairs:
                    delim_stack.append((tok.type, tok.lineno))
                elif tok.type in [pair[0] for pair in delim_pairs.values()]:
                    if not delim_stack:
                        errors.append(f"Unmatched closing delimiter '{tok.value}' at line {tok.lineno}")
                    else:
                        opening_type, _ = delim_stack.pop()
                        expected_closing = delim_pairs[opening_type][0]
                        if tok.type != expected_closing:
                            errors.append(f"Mismatched delimiters at line {tok.lineno}")

                tokens.append((tok.type, tok.value, tok.lineno))

            except Exception as e:
                errors.append(str(e))

        # Check for unclosed delimiters
        for delim_type, line_no in delim_stack:
            delim_char = delim_pairs[delim_type][1][0]
            errors.append(f"Unclosed delimiter '{delim_char}' from line {line_no}")

        if errors:
            raise Exception("\n".join(errors))

        return tokens




