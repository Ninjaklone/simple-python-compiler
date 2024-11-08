class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.scope_stack = [{}]  # Stack of scopes for nested blocks
        self.current_scope = self.scope_stack[-1]
        self.errors = []

    def analyze(self, ast):
        """Main entry point for semantic analysis"""
        try:
            self.visit_node(ast)
            return len(self.errors) == 0, self.errors
        except Exception as e:
            self.errors.append(str(e))
            return False, self.errors

    def visit_node(self, node):
        """Visit a node in the AST"""
        if not isinstance(node, dict):
            return
            
        method_name = f'visit_{node["type"].lower()}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Default visitor for nodes without specific visitors"""
        pass

    def visit_program(self, node):
        """Visit program node"""
        for statement in node['body']:
            self.visit_node(statement)

    def visit_assignment(self, node):
        """Check and record variable assignments"""
        name = node['name']
        value = self.visit_node(node['value'])
        
        # Record variable in symbol table
        self.current_scope[name] = {
            'type': self.infer_type(node['value']),
            'initialized': True,
            'value': value
        }

    def visit_functioncall(self, node):
        """Check function calls"""
        name = node['name']
        
        # Check if function exists
        if name not in self.symbol_table:
            self.errors.append(f"Undefined function '{name}'")
            return
            
        # Check arguments
        for arg in node['arguments']:
            self.visit_node(arg)

    def visit_printstatement(self, node):
        """Check print statement"""
        self.visit_node(node['expression'])

    def visit_returnstatement(self, node):
        """Check return statement"""
        self.visit_node(node['value'])

    def visit_literal(self, node):
        """Visit literal node"""
        return node['value']

    def visit_identifier(self, node):
        """Check identifier references"""
        name = node['name']
        
        # Check if variable is defined
        if name not in self.current_scope:
            self.errors.append(f"Undefined variable '{name}'")
            return None
            
        return self.current_scope[name]['value']

    def infer_type(self, node):
        """Infer the type of an expression"""
        if node['type'] == 'Literal':
            if 'dataType' in node:
                return node['dataType']
            # Fallback type inference
            value = node['value']
            if isinstance(value, int) or value.isdigit():
                return 'number'
            elif isinstance(value, str):
                return 'string'
            return 'unknown'
        elif node['type'] == 'Identifier':
            name = node['name']
            if name in self.current_scope:
                return self.current_scope[name]['type']
        return 'unknown'

    def enter_scope(self):
        """Enter a new scope"""
        new_scope = {}
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        """Exit current scope"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]

    def check_types(self, left_type, right_type, operation):
        """Check if types are compatible for an operation"""
        if left_type == 'unknown' or right_type == 'unknown':
            return True
            
        if operation in ['+', '-', '*', '/']:
            if left_type == 'number' and right_type == 'number':
                return True
            elif operation == '+' and left_type == 'string' and right_type == 'string':
                return True
                
        return False
