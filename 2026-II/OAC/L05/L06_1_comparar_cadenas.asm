; ---------------------------------------------------------------
; Programa: L06_1_comparar_cadenas.asm
;
; COMPILAR:   nasm -f elf32 L06_1_comparar_cadenas.asm -o L06_1_comparar_cadenas.o
; LINKEAR:    ld -m elf_i386 L06_1_comparar_cadenas.o -o L06_1_comparar_cadenas
; EJECUTAR:   ./L06_1_comparar_cadenas

; L06_1_comparar_cadenas.asm
; Tras ejecutar:  echo $?   -> 111 (iguales) o 100 (diferentes)
section .data
    msg1  db "Ingrese cadena 1: "
    len1  equ $ - msg1
    msg2  db "Ingrese cadena 2: "
    len2  equ $ - msg2
    m_ig  db "Resultado: Iguales", 10
    lm_ig equ $ - m_ig
    m_di  db "Resultado: Diferentes", 10
    lm_di equ $ - m_di

section .bss
    cad1 resb 64
    cad2 resb 64

section .text
global _start
_start:
    push len1
    push msg1
    call imprimir
    add  esp, 8
    push 64
    push cad1
    call leer_cadena
    add  esp, 8

    push len2
    push msg2
    call imprimir
    add  esp, 8
    push 64
    push cad2
    call leer_cadena
    add  esp, 8

    push cad2                   ; se apila en orden inverso
    push cad1
    call comparar_cadenas
    add  esp, 8
    mov  edi, eax               ; EDI = 111 o 100 (los procedimientos preservan EDI)

    cmp  edi, 111
    jne  .dif
    push lm_ig
    push m_ig
    jmp  .mostrar
.dif:
    push lm_di
    push m_di
.mostrar:
    call imprimir
    add  esp, 8

    mov  eax, 1                 ; sys_exit
    mov  ebx, edi               ; exit status = EAX del procedimiento -> $?
    int  0x80

; comparar_cadenas(s1, s2) -> EAX = 111 si iguales, 100 si no
comparar_cadenas:
    push ebp
    mov  ebp, esp
    push esi
    push edi
    mov  esi, [ebp+8]
    mov  edi, [ebp+12]
.loop:
    mov  al, [esi]
    cmp  al, [edi]
    jne  .dif
    test al, al                 ; ambas terminaron (0) a la vez
    je   .ig
    inc  esi
    inc  edi
    jmp  .loop
.ig:
    mov  eax, 111
    jmp  .fin
.dif:
    mov  eax, 100
.fin:
    pop  edi
    pop  esi
    pop  ebp
    ret

; leer_cadena(buf, max) -> EAX = longitud; quita el '\n' y termina en 0
leer_cadena:
    push ebp
    mov  ebp, esp
    push ebx
    mov  eax, 3
    xor  ebx, ebx
    mov  ecx, [ebp+8]
    mov  edx, [ebp+12]
    dec  edx                    ; deja lugar para el 0 final
    int  0x80
    mov  ecx, [ebp+8]
    test eax, eax
    jle  .vacio
    cmp  byte [ecx+eax-1], 10
    jne  .nul
    dec  eax
.nul:
    mov  byte [ecx+eax], 0
    jmp  .fin
.vacio:
    xor  eax, eax
    mov  byte [ecx], 0
.fin:
    pop  ebx
    pop  ebp
    ret

; parametros en pila, resultado en EAX
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
