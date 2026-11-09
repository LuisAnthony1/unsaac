; ---------------------------------------------------------------
; Programa: L06_3_fibonacci.asm
;
; COMPILAR:   nasm -f elf32 L06_3_fibonacci.asm -o L06_3_fibonacci.o
; LINKEAR:    ld -m elf_i386 L06_3_fibonacci.o -o L06_3_fibonacci
; EJECUTAR:   ./L06_3_fibonacci

section .data
    m_n   db "Ingrese n: "
    l_n   equ $ - m_n
    m_f1  db "Fibonacci("
    l_f1  equ $ - m_f1
    m_f2  db ") = "
    l_f2  equ $ - m_f2
    m_err db "n debe estar entre 0 y 40", 10
    l_err equ $ - m_err

section .text
global _start
_start:
    push l_n
    push m_n
    call imprimir
    add  esp, 8
    call leer_numero
    cmp  eax, 40                ; sin signo: tambien rechaza negativos
    ja   .error
    mov  esi, eax               ; ESI = n (los procedimientos preservan ESI/EDI)

    push esi
    call fibonacci
    add  esp, 4
    mov  edi, eax               ; EDI = resultado

    push l_f1
    push m_f1
    call imprimir
    add  esp, 8
    push esi
    call imprimir_numero
    add  esp, 4
    push l_f2
    push m_f2
    call imprimir
    add  esp, 8
    push edi
    call imprimir_numero
    add  esp, 4
    push 1
    push nl
    call imprimir
    add  esp, 8
    xor  ebx, ebx
    jmp  .salir
.error:
    push l_err
    push m_err
    call imprimir
    add  esp, 8
    mov  ebx, 1
.salir:
    mov  eax, 1
    int  0x80

; fibonacci(n) -> EAX = F(n):  F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
fibonacci:
    push ebp
    mov  ebp, esp
    push ebx                    ; EBX guarda F(n-1) durante la 2da llamada
    mov  eax, [ebp+8]
    cmp  eax, 1
    jbe  .base                  ; n = 0 o 1 -> devuelve n
    dec  eax
    push eax
    call fibonacci              ; F(n-1)
    add  esp, 4
    mov  ebx, eax
    mov  eax, [ebp+8]
    sub  eax, 2
    push eax
    call fibonacci              ; F(n-2)
    add  esp, 4
    add  eax, ebx
.base:
    pop  ebx
    pop  ebp
    ret

; cdecl: parametros en pila, resultado en EAX
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
