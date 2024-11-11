from ir_generator import IRGenerator
from typing import List, Dict, Any, Optional
class CodeGenerator:
    def __init__(self):
        self.instructions: List[str] = []
        self.data_section: Dict[str, Any] = {}  # Store variable names and their values
        self.temp_counter: int = 0

    def generate(self, ir: List[str]) -> str:
        """Generate NASM assembly code from IR"""
        self.instructions = []
        self.data_section = {}
        self.instructions.append("section .data")
        
        # Generate the data section for variables
        for var_name, var_value in self.data_section.items():
            if isinstance(var_value, int):
                self.instructions.append(f"{var_name} dd {var_value}")  # Define a double word for integers
            elif isinstance(var_value, str):
                self.instructions.append(f"{var_name} db '{var_value}', 0")  # Define a string with null terminator

        self.instructions.append("\nsection .text")
        self.instructions.append("global _start")
        self.instructions.append("_start:")

        for instruction in ir:
            self.visit_instruction(instruction)

        # Add exit syscall
        self.instructions.append("mov eax, 60")  # syscall for exit
        self.instructions.append("xor ebx, ebx")  # return code 0
        self.instructions.append("int 0x80")  # call kernel

        return "\n".join(self.instructions)

    def visit_instruction(self, instruction: str) -> None:
        """Process an IR instruction"""
        parts = instruction.split()
        print(parts)
        opcode = parts[0]

        if opcode == "STORE":
            self.handle_store(parts)
        elif opcode == "PRINT":
            self.handle_print(parts)
        elif parts[0] in {'ADD', 'SUB', 'MUL', 'DIV'}:
            self.handle_binary_operation(parts)
        elif opcode == "LOAD":
            self.handle_load(parts)

    def handle_store(self, parts: List[str]) -> None:
        """Handle store instruction"""
        _, src, dest = parts
        self.instructions.append(f"mov {dest}, {src}")

    def handle_print(self, parts: List[str]) -> None:
        """Handle print instruction"""
        _, *args = parts
        for arg in args:
            # Assuming args are variable names
            self.instructions.append(f"mov eax, 4")  # syscall for write
            self.instructions.append(f"mov ebx, 1")  # file descriptor (stdout)
            self.instructions.append(f"mov ecx, {arg}")  # address of string
            self.instructions.append(f"mov edx, 4")  # number of bytes (this should be the length of the string)
            self.instructions.append(f"int 0x80")  # call kernel

    def handle_binary_operation(self, parts: List[str]) -> None:
        """Handle binary operations"""
        op = parts[0]
        result = parts[1]
        left = parts[2]
        right = parts[3]

        if op == "ADD":
            self.instructions.append(f"mov eax, {left}")
            self.instructions.append(f"add eax, {right}")
            self.instructions.append(f"mov {result}, eax")
        elif op == "SUB":
            self.instructions.append(f"mov eax, {left}")
            self.instructions.append(f"sub eax, {right}")
            self.instructions.append(f"mov {result}, eax")
        elif op == "MUL":
            self.instructions.append(f"mov eax, {left}")
            self.instructions.append(f"imul eax, {right}")
            self.instructions.append(f"mov {result}, eax")
        elif op == "DIV":
            self.instructions.append(f"mov eax, {left}")
            self.instructions.append(f"xor edx, edx")  # clear edx before division
            self.instructions.append(f"div {right}")
            self.instructions.append(f"mov {result}, eax")

    def handle_load(self, parts: List[str]) -> None:
        """Handle load instruction"""
        _, temp, var_name = parts
        self.instructions.append(f"mov {temp}, {var_name}")

    def add_variable(self, name: str, value: Any) -> None:
        """Add a variable to the data section"""
        self.data_section[name] = value


# Example usage
ir_gen = IRGenerator()
ir = ir_gen.generate({
    'type': 'Program',
    'body': [
        {'type': 'Assignment', 'name': 'x', 'value': {'type': 'Literal', 'value': 5}},
        {'type': 'Assignment', 'name': 'y', 'value': {'type': 'Literal', 'value': 10}},
        {'type': 'FunctionCall', 'name': 'print', 'arguments': [{'type': 'Identifier', 'name': 'x'}]},
        {'type': 'FunctionCall', 'name': 'print', 'arguments': [{'type': 'Identifier', 'name': 'y'}]}
    ]
})

code_gen = CodeGenerator()
assembly_code = code_gen.generate(ir)
print(assembly_code)