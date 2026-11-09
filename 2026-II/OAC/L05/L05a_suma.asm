; ---------------------------------------------------------------
; Programa: L05a_suma.asm
;
; COMPILAR:   nasm -f elf32 L05a_suma.asm -o L05a_suma.o
; LINKEAR:    ld -m elf_i386 L05a_suma.o -o L05a_suma
; EJECUTAR:   ./L05a_suma

section .data
    msg1 db "Ingrese 1er número: "
    len1 equ $ - msg1
    msg2 db "Ingrese 2do número: "
    len2 equ $ - msg2
    msgr db "La suma es: "
    lenr equ $ - msgr

section .text
global _start
_start:
    push len1
    push msg1
    call imprimir
    add  esp, 8
    call leer_numero
    push eax                    ; a (queda en la pila)

    push len2
    push msg2
    call imprimir
    add  esp, 8
    call leer_numero
    push eax                    ; b  -> pila: [esp]=b, [esp+4]=a
    call sumar
    add  esp, 8                 ; limpia a y b

    push eax                    ; resultado
    push lenr
    push msgr
    call imprimir
    add  esp, 8
    call imprimir_numero        ; usa el resultado que sigue en la pila
    add  esp, 4
    push 1
    push nl
    call imprimir
    add  esp, 8

    mov  eax, 1                 ; sys_exit
    xor  ebx, ebx
    int  0x80

; sumar(a, b) -> EAX = a + b
sumar:
    push ebp
    mov  ebp, esp
    mov  eax, [ebp+8]
    add  eax, [ebp+12]
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
