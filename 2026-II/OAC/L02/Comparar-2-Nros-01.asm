; Programa: Comparar-2-Nros-01.asm
;
; Compilacion: nasm -f elf Comparar-2-Nros-01.asm -o Comparar-2-Nros-01.o
; Linkeado:    ld -m elf_i386 Comparar-2-Nros-01.o -o Comparar-2-Nros-01
 
section .data
  msj_mayor db 'A es mayor que B', 0xA
  long_mayor equ $ - msj_mayor
  msj_menor db 'A es menor o igual a B', 0xA
  long_menor equ $ - msj_menor
 
section .text
  global _start
 
_start:
  ; Valores para comparar
  mov eax, 150
  mov ebx, 2150
 
  ; Comparar los valores
  cmp eax, ebx
 
  ; Bifurcacion condicional
  jg  A_es_mayor
  jle A_es_menor
 
A_es_mayor:
  mov eax, 4
  mov ebx, 1
  mov ecx, msj_mayor
  mov edx, long_mayor
  int 0x80
  jmp salir
 
A_es_menor:
  mov eax, 4
  mov ebx, 1
  mov ecx, msj_menor
  mov edx, long_menor
  int 0x80
 
salir:
  mov eax, 1
  xor ebx, ebx
  int 0x80
