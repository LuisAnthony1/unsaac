; Programa: Hola-Mundo-x3.asm
;
; Descripcion: Imprime "Hola Mundo" 3 veces usando un bucle controlado por
;              contador (LOOP). Como ECX tambien se usa como puntero en la
;              syscall sys_write, se preserva el contador con PUSH/POP.
;
; Compilacion: nasm -f elf Hola-Mundo-x3.asm -o Hola-Mundo-x3.o
; Linkeado:    ld -m elf_i386 Hola-Mundo-x3.o -o Hola-Mundo-x3
; Ejecucion:   ./Hola-Mundo-x3

section .data
  msj db "Hola Mundo", 10
  longitud equ $ - msj

section .text
  global _start

_start:
  mov ecx, 3                 ; contador de repeticiones

ciclo:
  push ecx                    ; preservar el contador (ECX se usa como
                               ; puntero al mensaje dentro de la syscall)

  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, longitud
  int 0x80

  pop ecx                      ; restaurar el contador
  loop ciclo                    ; ECX -= 1 y repite si ECX != 0

  ; Salir
  mov eax, 1
  xor ebx, ebx
  int 0x80
