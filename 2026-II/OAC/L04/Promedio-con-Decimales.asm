; Programa: Promedio-con-Decimales.asm
;
; Descripcion: Calcula el promedio de [5, 15, 25, 35] y lo imprime como
;              entero y fraccion (1 decimal), por ejemplo "20.0".
;              Parte entera = suma / len ; primer decimal = (residuo*10) / len
;
; Compilacion: nasm -f elf Promedio-con-Decimales.asm -o Promedio-con-Decimales.o
; Linkeado:    ld -m elf_i386 Promedio-con-Decimales.o -o Promedio-con-Decimales
; Ejecucion:   ./Promedio-con-Decimales

section .data
  arreglo dd 5, 15, 25, 35
  len equ ($ - arreglo)/4
  msj db "El promedio es: "
  longitud equ $ - msj
  punto db '.'
  NL db 10

section .bss
  buffer resb 12

section .text
  global _start

_start:
  ; --- calcular la suma de los elementos ---
  mov esi, 0
  mov ecx, len
  mov ebx, 0

sumar:
  add ebx, [arreglo + esi*4]
  inc esi
  loop sumar
  ; EBX = suma total

  ; --- calcular parte entera y residuo: EAX = suma/len, EDX = suma%len ---
  mov eax, ebx
  mov ecx, len
  xor edx, edx
  div ecx

  mov esi, eax                  ; esi = parte entera (preservar)
  mov edi, edx                   ; edi = residuo (preservar)

  ; imprimir el mensaje
  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, longitud
  int 0x80

  ; imprimir la parte entera
  mov eax, esi
  call imprimir_numero

  ; imprimir el punto decimal
  mov eax, 4
  mov ebx, 1
  mov ecx, punto
  mov edx, 1
  int 0x80

  ; calcular el primer decimal: frac = (residuo * 10) / len
  mov eax, edi
  imul eax, 10
  xor edx, edx
  mov ebx, len
  div ebx

  call imprimir_numero          ; imprime el digito de la fraccion

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
