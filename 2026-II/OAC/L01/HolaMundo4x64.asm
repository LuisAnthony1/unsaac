; Programa: HolaMundo4x64.asm
;
; Compilacion: nasm -f elf64 HolaMundo4x64.asm -o HolaMundo4x64.o
;		Linkeado: ld HolaMundo4x64.o -o HolaMundo4x64

	global _start 								; punto de inicio del Programa

section .text
_start:

	mov 	rax,1
	mov 	rdi, 1
	mov 	rsi, msj
	mov 	rdx, 14
	syscall
	
	mov 	rax, 60
	xor		rdi, rdi
	syscall
	
section .data
	msj: 	db "Hola Mundo 4!", 10