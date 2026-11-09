; Programa: Uso-de-MOV-LEA-01-parte1.asm
;
; Descripcion: Carga el 3er elemento (indice 2) de 'arreglo' en un registro
;              usando LEA + MOV, lo copia a la variable 'var' y lo imprime
;              en consola SIN hacer ninguna conversion (se escriben los
;              4 bytes crudos del entero tal cual estan en memoria).
;
; Compilacion: nasm -f elf Uso-de-MOV-LEA-01-parte1.asm -o Uso-de-MOV-LEA-01-parte1.o
;   Linkeado:  ld -m elf_i386 Uso-de-MOV-LEA-01-parte1.o -o Uso-de-MOV-LEA-01-parte1
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte1
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte1 | od -An -tx1 -c   ; para ver bytes crudos

section .data
	arreglo 	dd 10, 20, 50, 80 
	var     	dd 0                       

section .text
	global _start                      

_start:
	; Usar LEA para calcular la direccion del 3er elemento:
	LEA ESI, [arreglo + 8]

	; Usar MOV para obtener su valor
	MOV EAX, [ESI]

	; cargar 'var'
	MOV [var], EAX

	;imprimi 'var'
	MOV EAX, 4
	MOV EBX, 1
	MOV ECX, var
	MOV EDX, 4
	INT 0x80

	; Salir
	MOV EAX, 1
	XOR EBX, EBX
	INT 0x80
