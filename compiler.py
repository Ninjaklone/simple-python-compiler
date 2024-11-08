from typing import List, Dict, Any, Tuple
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.ir_generator = IRGenerator()
        self.optimizer = Optimizer()
        self.code_generator = CodeGenerator()
    
    def compile(self, source_code: str) -> Tuple[bool, str]:
        try:
            # Lexical Analysis
            tokens = self.lexer.lexerFunc(source_code)
            if not tokens:
                return False, "Lexical analysis failed: No tokens generated"
            
            # Parsing
            ast = self.parser.parse(tokens)
            if not ast:
                return False, "Parsing failed: No AST generated"
            
            # Semantic Analysis
            # success, errors = self.semantic_analyzer.analyze(ast)
            # if not success:
            #     error_msg = "Semantic analysis failed:\n" + "\n".join(errors)
            #     return False, error_msg
            
            # IR Generation
            ir = self.ir_generator.generate(ast)
            if not ir:
                return False, "IR generation failed: No IR generated"
            
            # Optimization
            optimized_ir = self.optimizer.optimize(ir)
            if not optimized_ir:
                return False, "Optimization failed"
            
            # Code Generation
            assembly = self.code_generator.generate(optimized_ir)
            if not assembly:
                return False, "Code generation failed: No assembly generated"
            
            return True, assembly
            
        except Exception as e:
            return False, f"Compilation error: {str(e)}"

def main():
    compiler = Compiler()
    source_code = """
    x = 42
    print(x)
    """
    
    success, result = compiler.compile(source_code)
    if success:
        print("Compilation successful!")
        print("Generated assembly:")
        print(result)
    else:
        print("Compilation failed:")
        print(result)

if __name__ == "__main__":
    main()
