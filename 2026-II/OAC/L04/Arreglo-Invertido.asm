; Programa: Arreglo-Invertido.asm
;
; Descripcion: Invierte el arreglo [10, 20, 30, 40] e imprime el resultado
;              (recorriendolo del ultimo al primer elemento).
;              Salida esperada: 40 30 20 10
;
; Compilacion: nasm -f elf Arreglo-Invertido.asm -o Arreglo-Invertido.o
; Linkeado:    ld -m elf_i386 Arreglo-Invertido.o -o Arreglo-Invertido
; Ejecucion:   ./Arreglo-Invertido

section .data
  arreglo dd 10, 20, 30, 40
  len equ ($ - arreglo)/4
  espacio db ' '
  NL db 10

section .bss
  buffer resb 12               ; buffer para convertir cada numero a ASCII

section .text
  global _start

_start:
  mov esi, len
  dec esi                       ; esi = indice del ultimo elemento

recorrer:
  mov eax, [arreglo + esi*4]     ; cargar elemento actual (de atras hacia adelante)
  call imprimir_numero

  cmp esi, 0
  je fin_recorrido

  ; imprimir espacio separador
  mov eax, 4
  mov ebx, 1
  mov ecx, espacio
  mov edx, 1
  int 0x80

  dec esi
  jmp recorrer

fin_recorrido:
  mov eax, 4
  mov ebx, 1
  mov ecx, NL
  mov edx, 1
  int 0x80

  mov eax, 1
  xor ebx, ebx
  int 0x80

; ---------------------------------------------------------------------------
; Subrutina: imprimir_numero
; Convierte el valor entero en EAX a cadena decimal ASCII y lo imprime.
; Preserva todos los registros que usa (incluido ESI, el indice del arreglo).
; ---------------------------------------------------------------------------
imprimir_numero:
  push esi
  push edi
  push ebx
  push ecx
  push edx

  mov edi, buffer + 12          ; ancla: un byte PASADO el final del buffer
  mov ebx, 10

.convertir:
  dec edi
  xor edx, edx
  div ebx
  add dl, '0'
  mov [edi], dl
  test eax, eax
  jnz .convertir

  mov ecx, buffer + 12
  sub ecx, edi                  ; ecx = longitud de la cadena

  mov edx, ecx
  mov ecx, edi
  mov eax, 4
  mov ebx, 1
  int 0x80

  pop edx
  pop ecx
  pop ebx
  pop edi
  pop esi
  ret
