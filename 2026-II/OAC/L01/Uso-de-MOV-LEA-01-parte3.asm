; Programa: Uso-de-MOV-LEA-01-parte3.asm
;
; Descripcion: Se agrega el valor \u263a (caracter Unicode SMILING FACE, ☺)
;              al final del 'arreglo' ya actualizado (queda como el 6to
;              elemento, indice 5). Como 'arreglo' esta declarado con DD
;              (enteros de 32 bits), lo que se guarda es el VALOR NUMERICO
;              del code point Unicode (0x263A = 9786), NO su codificacion
;              UTF-8. Se carga con LEA + MOV, se copia a 'var' y se imprime
;              SIN conversion (bytes crudos).
;
; Compilacion: nasm -f elf Uso-de-MOV-LEA-01-parte3.asm -o Uso-de-MOV-LEA-01-parte3.o
;   Linkeado:  ld -m elf_i386 Uso-de-MOV-LEA-01-parte3.o -o Uso-de-MOV-LEA-01-parte3
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte3
;   Ejecucion: ./Uso-de-MOV-LEA-01-parte3 | od -An -tx1 -c   ; para ver bytes crudos

section .data
	arreglo dd 10, 20, 50, 80, 119, 0x263A  ; se agrego el codepoint U+263A (☺)
																		; [0]=10,[1]=20,[2]=50,[3]=80,
																		; [4]=119,[5]=0x263A (9786 decimal)
	var     	dd 0                             					; variable de 32 bits para el resultado

section .text
	global _start

_start:
	; Direccion del nuevo (6to) elemento: arreglo[5]
	LEA ESI, [arreglo + 20]            	; offset = 5 * 4 bytes = 20
														; ESI = direccion de arreglo[5]

	; Obtener su valor
	MOV EAX, [ESI]                     		; EAX = 0x0000263A

	; cargar 'var'
	MOV [var], EAX                     		; var = 0x0000263A

	; Imprimir 'var' (sys_write, SIN conversion)
	MOV EAX, 4                         		; sys_write (kernel opcode: 4)
	MOV EBX, 1                         		; fd = 1 (stdout)
	MOV ECX, var                       		; direccion de 'var'
	MOV EDX, 4                         		; 4 bytes (un dword completo)
	INT 0x80                           			; Llamada al Kernel

	; Salir del programa
	MOV EAX, 1                         		; sys_exit (kernel opcode: 1)
	XOR EBX, EBX                       	; status = 0 (Sin errores)
	INT 0x80

; ---------------------------------------------------------------------------
; RESULTADO OBSERVADO (verificado en ejecucion real) / QUE SE ESTA MOSTRANDO:
;   Bytes impresos: 3A 26 00 00  (little-endian de 0x0000263A)
;   Esto se traduce como los caracteres ASCII ':' (0x3A) y '&' (0x26),
;   seguidos de 2 bytes nulos. EN CONSOLA NO SE VE EL SMILEY (☺).
;
;   Por que: el emoji/caracter ☺ en UTF-8 se representa con 3 bytes
;   (0xE2 0x98 0xBA), NO como un entero de 4 bytes con el valor numerico
;   del code point (9786). Al declarar "dd 0x263A" estamos guardando el
;   NUMERO 9786 en little-endian, y como no se hizo ninguna conversion,
;   la terminal interpreta esos 4 bytes crudos como caracteres ASCII/
;   Latin-1 individuales -> de ahi ":&" + nulos, en vez del simbolo ☺.
;   Para mostrar realmente ☺ habria que declarar los bytes UTF-8 con DB
;   (db 0xE2, 0x98, 0xBA) e imprimirlos en una terminal que interprete UTF-8.
; ---------------------------------------------------------------------------