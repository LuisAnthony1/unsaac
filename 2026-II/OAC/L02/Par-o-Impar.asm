; Programa: Par-o-Impar.asm
;
; Descripcion: Determina si 'numero' es par o impar usando TEST y JZ.
;              El resultado se guarda en EDI (1 = impar, 0 = par).
;
; Compilacion: nasm -f elf Par-o-Impar.asm -o Par-o-Impar.o
; Linkeado:    ld -m elf_i386 Par-o-Impar.o -o Par-o-Impar
 
section .data
  numero dd 20
  msj_par   db 'El numero es PAR', 0xA
  long_par  equ $ - msj_par
  msj_impar db 'El numero es IMPAR', 0xA
  long_impar equ $ - msj_impar
 
section .text
  global _start
 
_start:
  ; Verificar la paridad
  test dword [numero], 1
  jz es_par
 
es_impar:
  mov edi, 1
  mov eax, 4
  mov ebx, 1
  mov ecx, msj_impar
  mov edx, long_impar
  int 0x80
  jmp salir
 
es_par:
  mov edi, 0
  mov eax, 4
  mov ebx, 1
  mov ecx, msj_par
  mov edx, long_par
  int 0x80
 
salir:
  mov eax, 1
  xor ebx, ebx
  int 0x80
