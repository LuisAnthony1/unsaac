; Compilación: nasm -f elf32 Lab06_Propuesto1_Sub.asm
section .text
global multiplicar

multiplicar:
    push ebp
    mov ebp, esp
    
    mov eax, [ebp+8]    
    imul eax, [ebp+12]  
    
    pop ebp
    ret
    