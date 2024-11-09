class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return {'type': 'Program', 'body': statements}

    def parse_statement(self):
        if self.current_token >= len(self.tokens):
            return None
        
        token = self.tokens[self.current_token]
        
        if self.current_token + 1 < len(self.tokens) and self.tokens[self.current_token + 1][1] == '=':
            return self.parse_assignment()
        elif self.current_token + 1 < len(self.tokens) and self.tokens[self.current_token + 1][1] == '(':
            return self.parse_function_call()
        else:
            return self.parse_expression()

    def parse_assignment(self):
        var_name = self.tokens[self.current_token][1]
        self.current_token += 2  # Skip variable name and '='
        
        value = self.parse_expression()
        
        return {
            'type': 'Assignment',
            'name': var_name,
            'value': value
        }

    def parse_function_call(self):
        func_name = self.tokens[self.current_token][1]
        self.current_token += 2  # Skip function name and '('
        
        args = []
        while self.current_token < len(self.tokens):
            if self.tokens[self.current_token][1] == ')':
                self.current_token += 1
                break
            if self.tokens[self.current_token][1] == ',':
                self.current_token += 1
                continue
            args.append(self.parse_expression())
        
        return {
            'type': 'FunctionCall',
            'name': func_name,
            'arguments': args
        }

    def parse_expression(self):
        return self.parse_additive()

    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token < len(self.tokens) and self.tokens[self.current_token][1] in ['+', '-']:
            operator = self.tokens[self.current_token][1]
            self.current_token += 1
            right = self.parse_multiplicative()
            left = {
                'type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left

    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.current_token < len(self.tokens) and self.tokens[self.current_token][1] in ['*', '/']:
            operator = self.tokens[self.current_token][1]
            self.current_token += 1
            right = self.parse_primary()
            left = {
                'type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left

    def parse_primary(self):
        if self.current_token >= len(self.tokens):
            return None
            
        token = self.tokens[self.current_token]
        self.current_token += 1
        
        if token[0] == 'NUMBER':
            return {
                'type': 'Literal',
                'value': float(token[1]),
                'dataType': 'float' if isinstance(token[1], float) else 'int'
            }
        elif token[0] == 'STRING':
            return {
                'type': 'Literal',
                'value': token[1][1:-1],  # Remove quotes
                'dataType': 'string'
            }
        elif token[0] == 'IDENT':
            return {
                'type': 'Identifier',
                'name': token[1]
            }
        elif token[1] == '(':
            expr = self.parse_expression()
            if self.tokens[self.current_token][1] != ')':
                raise SyntaxError("Expected closing parenthesis")
            self.current_token += 1
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token[1]}") # type: ignore