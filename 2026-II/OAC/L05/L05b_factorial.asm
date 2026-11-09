; ---------------------------------------------------------------
; Programa: L05b_factorial.asm
;
; COMPILAR:   nasm -f elf32 L05b_factorial.asm -o L05b_factorial.o
; LINKEAR:    ld -m elf_i386 L05b_factorial.o -o L05b_factorial
; EJECUTAR:   ./L05b_factorial

section .data
    msg  db "Ingrese un número (0-12): "
    len  equ $ - msg
    msgr db "El factorial es: "
    lenr equ $ - msgr
    merr db "Número fuera de rango (0-12)", 10
    lenerr equ $ - merr

section .text
global _start
_start:
    push len
    push msg
    call imprimir
    add  esp, 8
    call leer_numero
    cmp  eax, 12                ; sin signo: tambien atrapa negativos
    ja   .error
    push eax
    call factorial
    add  esp, 4
    push eax
    push lenr
    push msgr
    call imprimir
    add  esp, 8
    call imprimir_numero
    add  esp, 4
    push 1
    push nl
    call imprimir
    add  esp, 8
    xor  ebx, ebx
    jmp  .salir
.error:
    push lenerr
    push merr
    call imprimir
    add  esp, 8
    mov  ebx, 1
.salir:
    mov  eax, 1
    int  0x80

; factorial(n) -> EAX = n!
factorial:
    push ebp
    mov  ebp, esp
    mov  ecx, [ebp+8]
    mov  eax, 1
.loop:
    cmp  ecx, 1
    jle  .fin
    imul eax, ecx
    dec  ecx
    jmp  .loop
.fin:
    pop  ebp
    ret

; ============ RUTINAS COMUNES (cdecl: parametros en pila, resultado en EAX) ============
section .data
    nl db 10

section .bss
    buf_in  resb 16
    buf_out resb 12

section .text

; imprimir(ptr, len)  -> [ebp+8]=ptr, [ebp+12]=len
imprimir:
    push ebp
    mov  ebp, esp
    push ebx                    ; EBX se debe preservar
    mov  eax, 4                 ; sys_write
    mov  ebx, 1                 ; stdout
    mov  ecx, [ebp+8]
    mov  edx, [ebp+12]
    int  0x80
    pop  ebx
    pop  ebp
    ret

; leer_numero() -> EAX = entero con signo leido de stdin
leer_numero:
    push ebp
    mov  ebp, esp
    push ebx
    push esi
    mov  eax, 3                 ; sys_read
    xor  ebx, ebx               ; stdin
    mov  ecx, buf_in
    mov  edx, 16
    int  0x80
    mov  esi, buf_in
    xor  eax, eax               ; acumulador
    xor  ebx, ebx               ; EBX = 1 si es negativo
    cmp  byte [esi], '-'
    jne  .loop
    mov  ebx, 1
    inc  esi
.loop:
    movzx edx, byte [esi]
    sub  edx, '0'
    cmp  edx, 9                 ; comparacion sin signo: descarta '\n', 0, letras
    ja   .fin
    imul eax, eax, 10
    add  eax, edx
    inc  esi
    jmp  .loop
.fin:
    test ebx, ebx
    jz   .ret
    neg  eax
.ret:
    pop  esi
    pop  ebx
    pop  ebp
    ret

; imprimir_numero(n) -> [ebp+8]=n (entero con signo), lo imprime en decimal
imprimir_numero:
    push ebp
    mov  ebp, esp
    push ebx
    push esi
    push edi
    mov  eax, [ebp+8]
    xor  esi, esi               ; ESI = 1 si negativo
    test eax, eax
    jns  .pos
    neg  eax
    mov  esi, 1
.pos:
    lea  edi, [buf_out+12]      ; un byte despues del final
    mov  ebx, 10
.dig:
    xor  edx, edx
    div  ebx                    ; EAX = cociente, EDX = residuo
    add  dl, '0'
    dec  edi
    mov  [edi], dl
    test eax, eax
    jnz  .dig
    test esi, esi
    jz   .out
    dec  edi
    mov  byte [edi], '-'
.out:
    mov  ecx, edi
    lea  edx, [buf_out+12]
    sub  edx, ecx               ; longitud
    mov  eax, 4
    mov  ebx, 1
    int  0x80
    pop  edi
    pop  esi
    pop  ebx
    pop  ebp
    ret
