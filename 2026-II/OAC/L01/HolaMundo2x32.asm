; Programa: HolaMundo2x32.asm
;
; Compilacion: nasm -f elf HolaMundo2x32.asm -o HolaMundo2x32.o
;		Linkeado: ld -m elf_i386 HolaMundo2x32.o -o HolaMundo2x32

	global _start 								; punto de inicio del Programa

section .data
	msj: db 'Hola Mundo, Linux 2!'  	; El mensaje
	 
section .text

_start:

	; configurar los registros para sys_write: msj
	mov 	eax, 4
	mov 	ebx, 1
	mov 	ecx, msj
	mov 	edx, 20
	int 		0x80
	
	; Configurar los registros para sys_write : LF
	mov 	eax, 4
	mov 	ebx, 1
	mov 	ecx, LF
	mov 	edx, 1
	int 		0x80
	
	; exit del programa usando el system call sys_exit
	mov 	eax, 1
	xor 		ebx, ebx
	int 		0x80
	
section .data
	LF 		db 10