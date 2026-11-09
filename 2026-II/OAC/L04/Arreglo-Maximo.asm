; Programa: Arreglo-Maximo.asm
;
; Descripcion: Encuentra el elemento maximo en [500, 300, 900, 200] e
;              imprime "El maximo es: 900".
;
; Compilacion: nasm -f elf Arreglo-Maximo.asm -o Arreglo-Maximo.o
; Linkeado:    ld -m elf_i386 Arreglo-Maximo.o -o Arreglo-Maximo
; Ejecucion:   ./Arreglo-Maximo

section .data
  arreglo dd 500, 300, 900, 200
  len equ ($ - arreglo)/4
  msj db "El maximo es: "
  longitud equ $ - msj
  NL db 10

section .bss
  buffer resb 12

section .text
  global _start

_start:
  mov eax, [arreglo]           ; inicializar el maximo con el 1er elemento
  mov esi, 1                    ; siguiente indice a revisar

comparar:
  cmp esi, len
  jge fin_comparar

  mov ebx, [arreglo + esi*4]
  cmp ebx, eax
  jle no_actualizar
  mov eax, ebx                  ; se encontro un nuevo maximo

no_actualizar:
  inc esi
  jmp comparar

fin_comparar:
  mov edi, eax                  ; preservar el maximo (EAX se reutiliza)

  ; imprimir el mensaje
  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, longitud
  int 0x80

  ; imprimir el maximo
  mov eax, edi
  call imprimir_numero

  ; salto de linea
  mov eax, 4
  mov ebx, 1
  mov ecx, NL
  mov edx, 1
  int 0x80

  mov eax, 1
  xor ebx, ebx
  int 0x80

; ---------------------------------------------------------------------------
; Subrutina: imprimir_numero (misma tecnica que en Arreglo-Invertido.asm)
; ---------------------------------------------------------------------------
imprimir_numero:
  push esi
  push edi
  push ebx
  push ecx
  push edx

  mov edi, buffer + 12
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
  sub ecx, edi

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
