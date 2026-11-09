; ---------------------------------------------------------------
; Programa: L06_2_promedio.asm
;
; COMPILAR:   nasm -f elf32 L06_2_promedio.asm -o L06_2_promedio.o
; LINKEAR:    ld -m elf_i386 L06_2_promedio.o -o L06_2_promedio
; EJECUTAR:   ./L06_2_promedio

; L06_2_promedio.asm -- procedimiento con variables locales en el stack frame
section .data
    m1 db "Ingrese número 1: "
    l1 equ $ - m1
    m2 db "Ingrese número 2: "
    l2 equ $ - m2
    m3 db "Ingrese número 3: "
    l3 equ $ - m3
    mr db "El promedio es: "
    lr equ $ - mr

section .text
global _start
_start:
    call calculadora_promedio
    mov  eax, 1
    xor  ebx, ebx
    int  0x80

calculadora_promedio:
    push ebp
    mov  ebp, esp
    sub  esp, 12                ; 3 variables locales: [ebp-4], [ebp-8], [ebp-12]

    push l1
    push m1
    call imprimir
    add  esp, 8
    call leer_numero
    mov  [ebp-4], eax

    push l2
    push m2
    call imprimir
    add  esp, 8
    call leer_numero
    mov  [ebp-8], eax

    push l3
    push m3
    call imprimir
    add  esp, 8
    call leer_numero
    mov  [ebp-12], eax

    push dword [ebp-12]         ; parametros por la pila
    push dword [ebp-8]
    push dword [ebp-4]
    call promedio3
    add  esp, 12

    push eax
    push lr
    push mr
    call imprimir
    add  esp, 8
    call imprimir_numero
    add  esp, 4
    push 1
    push nl
    call imprimir
    add  esp, 8

    mov  esp, ebp               ; libera locales
    pop  ebp
    ret

; promedio3(a, b, c) -> EAX = (a+b+c)/3 (division entera con signo)
promedio3:
    push ebp
    mov  ebp, esp
    mov  eax, [ebp+8]
    add  eax, [ebp+12]
    add  eax, [ebp+16]
    cdq                         ; extiende signo a EDX:EAX
    mov  ecx, 3
    idiv ecx
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
