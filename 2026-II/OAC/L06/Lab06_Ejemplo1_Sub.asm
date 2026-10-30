; Compilación: nasm -f elf32 Lab06_Ejemplo1_Sub.asm
section .note.GNU-stack noalloc noexec nowrite progbits ; Marca la pila como no ejecutable
section .text
global suma_nasm

suma_nasm:
    push ebp
    mov ebp, esp
    
    mov eax, [ebp+8]     ; Carga el primer argumento (a) en EAX
    add eax, [ebp+12]    ; Suma el segundo argumento (b) a EAX
    
    pop ebp
    ret
    