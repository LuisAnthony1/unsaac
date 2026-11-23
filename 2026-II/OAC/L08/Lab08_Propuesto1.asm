; Programa: Lab08_Propuesto1.asm
; Compilación: ~$ nasm -f elf64 Lab08_Propuesto1.asm
;     Linkeado: ~$ ld Lab08_Propuesto1.o -o Lab08_Propuesto1
;     Ejecución: ~$ ./Lab08_Propuesto1

section .data
	msj_entrada  db "Ingrese una palabra o frase de 40 caracteres: "
	len_entrada  equ $ - msj_entrada
	msj_si       db "Es un palindromo.", 10
	len_si       equ $ - msj_si
	msj_no       db "No es un palindromo.", 10
	len_no       equ $ - msj_no
	msj_error    db "Error: la entrada excede los 40 caracteres.", 10
	len_error    equ $ - msj_error

section .bss
	buffer       resb 128

section .text
	global _start

_start:
	; mensaje de entrada
	mov rax, 1
	mov rdi, 1
	mov rsi, msj_entrada
	mov rdx, len_entrada
	syscall

	; cadena desde stdin
	mov rax, 0
	mov rdi, 0
	mov rsi, buffer
	mov rdx, 128
	syscall

	; salto de línea al final
	mov rcx, rax
.trim:
	cmp rcx, 0
	jle .verificar_longitud
	mov al, [buffer + rcx - 1]
	cmp al, 10
	je .quitar_char
	cmp al, 13
	je .quitar_char
	jmp .verificar_longitud

.quitar_char:
	dec rcx
	jmp .trim

.verificar_longitud:
	cmp rcx, 40
	jg .error_longitud
	cmp rcx, 0
	je .no_palindromo

	xor rsi, rsi
	mov rdi, rcx
	dec rdi

.comparar:
	cmp rsi, rdi
	jge .es_palindromo
	mov al, [buffer + rsi]
	mov dl, [buffer + rdi]
	cmp al, dl
	jne .no_palindromo
	inc rsi
	dec rdi
	jmp .comparar

.es_palindromo:
	mov rax, 1
	mov rdi, 1
	mov rsi, msj_si
	mov rdx, len_si
	syscall
	jmp .salir

.no_palindromo:
	mov rax, 1
	mov rdi, 1
	mov rsi, msj_no
	mov rdx, len_no
	syscall
	jmp .salir

.error_longitud:
	mov rax, 1
	mov rdi, 1
	mov rsi, msj_error
	mov rdx, len_error
	syscall

.salir:
	mov rax, 60
	xor rdi, rdi
	syscall

section .note.GNU-stack noalloc noexec nowrite progbits
