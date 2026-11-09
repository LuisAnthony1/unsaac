; Compilación: nasm -f elf32 Lab06_Ejemplo1_Sub.asm
section .note.GNU-stack noalloc noexec nowrite progbits ; pila como no ejecutable
section .text
global suma_nasm

suma_nasm:
    push ebp
    mov ebp, esp
    
    mov eax, [ebp+8]     ; carga (a) en EAX
    add eax, [ebp+12]    ; suma (b) a EAX
    
    pop ebp
    ret
    