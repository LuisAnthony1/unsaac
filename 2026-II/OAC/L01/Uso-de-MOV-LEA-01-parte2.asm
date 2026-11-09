; Programa: Uso-de-MOV-LEA-01-parte2.asm
;
; Descripcion: Se agrega el valor 119 al final de 'arreglo' (queda como el
;              5to elemento, indice 4). Se carga ese nuevo elemento en un
;              registro con LEA + MOV, se copia a 'var' y se imprime en
;              consola SIN conversion (bytes crudos del entero).
;
; Compilacion: nasm -f elf Uso-de-MOV-LEA-01-parte2.asm -o Uso-de-MOV-LEA-01-parte2.o
;   Linkeado:  ld -m elf_i386 Uso-de-MOV-LEA-01-parte2.o -o Uso-de-MOV-LEA-01-parte2
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte2
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte2 | od -An -tx1 -c   ; para ver bytes crudos

section .data
	arreglo dd 10, 20, 50, 80, 119
	var     	dd 0

section .text
  global _start

_start:
	; Direccion del nuevo (5to) elemento: arreglo[4] 
	LEA ESI, [arreglo + 16]

	; Obtener su valor
	MOV EAX, [ESI]

	; cargar 'var'
	MOV [var], EAX

	; Imprimir 'var' (sys_write, SIN conversion)
	MOV EAX, 4
	MOV EBX, 1
	MOV ECX, var
	MOV EDX, 4
	INT 0x80

	; Salir del programa
	MOV EAX, 1
	XOR EBX, EBX
	INT 0x80
