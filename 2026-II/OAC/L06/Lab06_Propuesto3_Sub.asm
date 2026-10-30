; Compilación: nasm -f elf32 Lab06_Propuesto3_Sub.asm
section .text
global potencia

potencia:
    push ebp
    mov ebp, esp
    push ebx            ; Preservar el registro EBX según la convención cdecl
    
    mov ebx, [ebp+8]    ; Cargar la base
    mov ecx, [ebp+12]   ; Cargar el exponente
    mov eax, 1          ; Inicializar el resultado en 1

.ciclo:
    cmp ecx, 0          ; Verificar si el exponente llegó a 0
    je .fin             ; Si es 0, saltar al final
    imul eax, ebx       ; Multiplicar el resultado actual por la base
    dec ecx             ; Disminuir el exponente en 1
    jmp .ciclo          ; Repetir el ciclo

.fin:
    pop ebx             ; Restaurar EBX
    pop ebp
    ret                 ; Retornar a C (resultado almacenado en EAX)
    