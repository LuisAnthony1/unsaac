; Compilación: nasm -f elf32 Lab06_Ejemplo2_Main.asm
; Linkeado: gcc -m32 Lab06_Ejemplo2_Main.o Lab06_Ejemplo2_Sub.o -o Lab06_Ejemplo2_Main -no-pie
; Ejecución: ./Lab06_Ejemplo2_Main
section .data
    msj1 db "Ingrese el primer numero: ", 0
    msj2 db "Ingrese el segundo numero: ", 0
    fmt_entrada db "%d", 0
    fmt_salida db "La suma es: %d", 10, 0

section .bss
    num1 resd 1
    num2 resd 1

section .text
extern printf, scanf, sumar
global main

main:
    ; Mostrar mensaje y leer ler número
    push msj1
    call printf
    add esp, 4

    push num1
    push fmt_entrada
    call scanf
    add esp, 8

    ; Mostrar mensaje y leer segundo número
    push msj2
    call printf
    add esp, 4

    push num2
    push fmt_entrada
    call scanf
    add esp, 8

    ; Obtener los valores leidos
    mov eax, [num1]
    mov ebx, [num2]

    ; Llamar a la función C: int sumar(int a, int b)
    push ebx
    push eax
    call sumar
    add esp, 8

    ; Imprimir resultado
    push eax
    push fmt_salida
    call printf
    add esp, 8

    ; Salida exitosa
    mov eax, 1
    mov ebx, 0
    int 0x80
    ret

section .note.GNU-stack noalloc noexec nowrite
