; Programa: Matriz-3x3.asm
;
; Descripcion: Usa un bucle anidado (ESI = fila i, EDI = columna j) para
;              generar e imprimir la matriz 3x3 donde cada elemento es
;              el producto i*j:
;                 1 2 3
;                 2 4 6
;                 3 6 9
;
; Compilacion: nasm -f elf Matriz-3x3.asm -o Matriz-3x3.o
; Linkeado:    ld -m elf_i386 Matriz-3x3.o -o Matriz-3x3
; Ejecucion:   ./Matriz-3x3

section .data
  espacio db ' '
  NL      db 10
  digito  db '0'             ; buffer de 1 caracter reutilizable

section .text
  global _start

_start:
  mov esi, 1                  ; i = 1 (fila)

fila:
  cmp esi, 3
  jg fin

  mov edi, 1                   ; j = 1 (columna)

columna:
  cmp edi, 3
  jg fin_columna

  ; --- calcular producto = i * j ---
  mov eax, esi
  imul eax, edi                 ; EAX = i*j (valor entre 1 y 9)

  ; --- convertir el digito a ASCII e imprimirlo ---
  add eax, '0'
  mov [digito], al
  mov eax, 4
  mov ebx, 1
  mov ecx, digito
  mov edx, 1
  int 0x80

  ; --- imprimir un espacio, salvo despues de la ultima columna ---
  cmp edi, 3
  jae saltar_espacio
  mov eax, 4
  mov ebx, 1
  mov ecx, espacio
  mov edx, 1
  int 0x80

saltar_espacio:
  inc edi
  jmp columna

fin_columna:
  ; --- imprimir salto de linea al terminar la fila ---
  mov eax, 4
  mov ebx, 1
  mov ecx, NL
  mov edx, 1
  int 0x80

  inc esi
  jmp fila

fin:
  ; Salir
  mov eax, 1
  xor ebx, ebx
  int 0x80
