class CodeGenerator:
    def __init__(self):
        self.assembly = []
        self.data_section = []
        self.text_section = []
        
    def generate(self, ir):
        """Generate assembly code from IR"""
        if not ir:
            return ""
            
        self.assembly = []
        self.generate_data_section()
        self.generate_text_section(ir)
        
        # Combine all sections
        result = "\n".join(self.data_section + ["\n"] + self.text_section)
        return result if result else ""
        
    def generate_data_section(self):
        """Generate data section of assembly"""
        self.data_section = ["section .data"]
        
    def generate_text_section(self, ir):
        """Generate text section of assembly"""
        self.text_section = [
            "section .text",
            "global _start",
            "_start:"
        ]
        
        for instruction in ir:
            assembly = self.translate_to_assembly(instruction)
            if assembly:
                self.text_section.extend(assembly)
                
        # Add exit syscall
        self.text_section.extend([
            "    mov eax, 1",      # exit syscall
            "    xor ebx, ebx",    # exit code 0
            "    int 0x80"         # make syscall
        ])
            
    def translate_to_assembly(self, instruction):
        """Convert IR instruction to assembly"""
        # Basic instruction translation
        if isinstance(instruction, str):
            parts = instruction.split()
            if parts[0] == 'PRINT':
                return [
                    f"    ; {instruction}",
                    f"    push {parts[1]}",
                    "    call print"
                ]
            elif parts[0] == 'STORE':
                return [
                    f"    ; {instruction}",
                    f"    mov [{parts[2]}], {parts[1]}"
                ]
            elif parts[0] == 'LOAD':
                return [
                    f"    ; {instruction}",
                    f"    mov {parts[1]}, [{parts[2]}]"
                ]
        return [f"    ; Unhandled: {instruction}"]