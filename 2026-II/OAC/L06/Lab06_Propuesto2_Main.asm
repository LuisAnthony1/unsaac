; Compilación: nasm -f elf32 Lab06_Propuesto2_Main.asm
; Linkeado: gcc -m32 Lab06_Propuesto2_Main.o Lab06_Propuesto2_Sub.o -o Lab06_Propuesto2_Main -no-pie
; Ejecución: ./Lab06_Propuesto2_Main
section .data
    msj db "Ingrese n: ", 0
    fmt_in db "%d", 0
    fmt_out db "El término Fibonacci de (%d) = %d", 10, 0

section .bss
    num resd 1

section .text
extern printf, scanf, fibonacci
global main

main:
    ; 1. Mostrar mensaje
    push msj
    call printf
    add esp, 4

    ; 2. Leer número n
    push num
    push fmt_in
    call scanf
    add esp, 8

    ; 3. Llamar a la función C fibonacci(n)
    mov eax, [num]
    push eax
    call fibonacci
    add esp, 4

    ; 4. Imprimir resultado
    push eax            ; apila el resultado (EAX)
    push dword [num]    ; apila n
    push fmt_out        ; apila formato
    call printf
    add esp, 12

    ; 5. Salir
    mov eax, 1
    mov ebx, 0
    int 0x80
    