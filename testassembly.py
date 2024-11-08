import os
import subprocess

def run_assembly():
    # Write assembly code using Windows calling convention
    asm_code = """section .data
    number_of_students db 90
    distance_in_meters dd 1000.0
    average_stride_length dd 0.78
    message db "The average number of steps required for each student to complete the walk is approximately: ", 0
    fmt db "%f", 10, 0  ; Format string for printf with newline

section .bss
    steps_per_student resd 1

section .text
    global _main
    extern _printf
    extern _exit

_main:
    ; Set up stack frame
    push ebp
    mov ebp, esp
    
    ; Load distance into FPU stack
    fld dword [distance_in_meters]
    fld dword [average_stride_length]
    
    ; Perform division
    fdivp st1, st0
    
    ; Store the result
    fstp dword [steps_per_student]
    
    ; Print message
    push message
    call _printf
    add esp, 4
    
    ; Print result
    fld dword [steps_per_student]
    sub esp, 8          ; Allocate space for double
    fstp qword [esp]    ; Store double value
    push fmt
    call _printf
    add esp, 12         ; Clean up stack
    
    ; Exit program
    xor eax, eax
    mov esp, ebp
    pop ebp
    ret"""
    
    # Write the assembly code to a file
    with open('program.asm', 'w') as f:
        f.write(asm_code)
    
    try:
        # Assemble using NASM
        subprocess.run(['nasm', '-f', 'win32', 'program.asm', '-o', 'program.obj'], check=True)
        
        # Link with Microsoft Linker (assuming MSVC is installed)
        subprocess.run(['link', '/subsystem:console', 'program.obj', 
                      '/defaultlib:msvcrt.lib', '/defaultlib:legacy_stdio_definitions.lib',
                      '/machine:x86'], check=True)
        
        # Execute the program
        result = subprocess.run(['program.exe'], capture_output=True, text=True)
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure you have the following installed:")
        print("1. NASM (Netwide Assembler)")
        print("2. Microsoft Visual Studio with C++ workload")
        print("3. Run this from the Visual Studio Developer Command Prompt")
    finally:
        # Clean up temporary files
        for file in ['program.asm', 'program.obj', 'program.exe']:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    run_assembly()