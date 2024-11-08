from typing import List, Dict, Any, Optional

class IRGenerator:
    def __init__(self):
        self.instructions: List[str] = []
        self.temp_counter: int = 0

    def generate(self, ast: Dict) -> List[str]:
        """Generate IR from AST"""
        self.instructions = []
        self.temp_counter = 0
        
        if isinstance(ast, dict) and ast.get('type') == 'Program':
            print("Processing Program Node")
            for statement in ast.get('body', []):
                self.visit_node(statement)
                
        return self.instructions

    def visit_node(self, node: Dict) -> Optional[str]:
        """Process an AST node"""
        if not isinstance(node, dict):
            print(f"Invalid node: {node}")
            return None
            
        node_type = node.get('type')
        if not node_type:
            print(f"Node has no type: {node}")
            return None
            
        print(f"Visiting node type: {node_type}")
        
        handlers = {
            'Assignment': self.handle_assignment,
            'FunctionCall': self.handle_function_call,
            'BinaryOperation': self.handle_binary_operation,
            'Literal': self.handle_literal,
            'Identifier': self.handle_identifier
        }
        
        handler = handlers.get(node_type)
        if handler:
            return handler(node)
        else:
            print(f"No handler for node type: {node_type}")
        return None

    def handle_assignment(self, node: Dict) -> None:
        """Handle assignment"""
        print(f"Generating assignment for: {node}")
        var_name = node['name']
        value_temp = self.visit_node(node['value'])
        if value_temp:
            self.emit(f"STORE {value_temp} {var_name}")

    def handle_function_call(self, node: Dict) -> Optional[str]:
        """Handle function call"""
        print(f"Generating function call for: {node}")
        func_name = node['name']
        if func_name == 'print':
            args_temps = []
            for arg in node.get('arguments', []):
                arg_temp = self.visit_node(arg)
                if arg_temp:
                    args_temps.append(arg_temp)
            self.emit(f"PRINT {' '.join(args_temps)}")
        return None

    def handle_binary_operation(self, node: Dict) -> Optional[str]:
        """Handle binary operation"""
        print(f"Generating binary operation for: {node}")
        left_temp = self.visit_node(node['left'])
        right_temp = self.visit_node(node['right'])
        if left_temp and right_temp:
            result_temp = self.new_temp()
            self.emit(f"{node['operator']} {result_temp} {left_temp} {right_temp}")
            return result_temp
        return None

    def handle_literal(self, node: Dict) -> Optional[str]:
        """Handle literal nodes"""
        print(f"Generating literal for: {node}")
        temp = self.new_temp()
        self.emit(f"LOAD {temp} {node['value']}")
        return temp

    def handle_identifier(self, node: Dict) -> Optional[str]:
        """Handle identifier nodes"""
        print(f"Generating identifier for: {node}")
        temp = self.new_temp()
        self.emit(f"LOAD {temp} {node['name']}")
        return temp

    def emit(self, instruction: str) -> None:
        """Add an instruction to the IR"""
        print(f"Emitting instruction: {instruction}")
        self.instructions.append(instruction)

    def new_temp(self) -> str:
        """Generate a new temporary variable name"""
        self.temp_counter += 1
        return f"t{self.temp_counter}"