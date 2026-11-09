; Programa: Tercer-Caracter-6.2.asm
;
; Descripcion: Muestra en consola el 3er caracter de una cadena/etiqueta
;              'mensaje' definida en .data, usando LEA para calcular la
;              direccion de ese caracter y sys_write para imprimir 1 solo
;              byte.
;
; Compilacion: nasm -f elf Tercer-Caracter-6.2.asm -o Tercer-Caracter-6.2.o
;   Linkeado:  ld -m elf_i386 Tercer-Caracter-6.2.o -o Tercer-Caracter-6.2
;   Ejecucion: ./Tercer-Caracter-6.2 
;   Ejecucion: ./Tercer-Caracter-6.2 | od -An -tx1 -c ; para ver bytes crudos

section .data
	mensaje db 'Buenos dias, Buenas tardes, Buenas noches', 10

section .text
	global _start

_start:
	; Direccion del 3er caracter: mensaje + 2
	LEA ESI, [mensaje + 2]

	; Imprimir el caracter usando sys_write
	MOV EAX, 4
	MOV EBX, 1
	MOV ECX, ESI
	MOV EDX, 1
	INT 0x80

	; Salir del programa
	MOV EAX, 1
	XOR EBX, EBX
	INT 0x80

; ---------------------------------------------------------------------------
; RESULTADO OBSERVADO (verificado en ejecucion real):
;   Salida en consola: e
;   (tercer caracter de "Buenos dias, Buenas tardes, Buenas noches", correcto)
;
;   NOTA: este mismo esquema funciona para cualquier 'mensaje' definido en
;   .data; solo hay que asegurarse de que tenga al menos 3 caracteres.
; ---------------------------------------------------------------------------