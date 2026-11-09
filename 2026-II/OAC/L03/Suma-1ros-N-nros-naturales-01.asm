; Programa: Suma-1ros-N-nros-naturales-01.asm
;
; Descripcion: Suma los primeros N numeros naturales usando LOOP,
;              luego convierte el resultado a cadena ASCII y lo imprime.
;
; Compilacion: nasm -f elf Suma-1ros-N-nros-naturales-01.asm -o Suma-1ros-N-nros-naturales-01.o
; Linkeado:    ld -m elf_i386 Suma-1ros-N-nros-naturales-01.o -o Suma-1ros-N-nros-naturales-01
; Ejecucion:   ./Suma-1ros-N-nros-naturales-01

section .data
  n        equ 50000
  msj      db "La suma es: "
  longitud equ $ - msj

section .bss
  buffer   resb 11              ; Buffer para almacenar el numero como cadena

section .text
  global _start

_start:
  ; Calcular suma
  mov ecx, n        ; ECX = n   (inicializar el contador)
  mov eax, 0          ; EAX = 0   (inicializar suma)
  mov ebx, 1            ; EBX = 1   (primer numero natural)

suma:
  add eax, ebx           ; EAX = EAX + EBX
  inc ebx                  ; EBX = EBX + 1
  loop suma                  ; ECX -= 1 y repite si ECX != 0

  ; Convertir numero a cadena
  mov edi, buffer + 10         ; Puntero al final del buffer
  mov byte [edi], 10            ; buffer[edi] = 10  (LF = salto de linea)
  dec edi                        ; EDI = EDI - 1
  mov ebx, 10                     ; Divisor = 10

convertir:
  xor edx, edx                     ; Pre-condicion para la division
  div ebx                           ; EAX = cociente, EDX = resto (1 digito)

  add dl, '0'                        ; Convertir el resto a ASCII
  mov [edi], dl                       ; buffer[edi] = digito
  dec edi                              ; Puntero actual adelantado
  test eax, eax                         ; ¿EAX == 0?
  jnz convertir

imprimir:
  ; Imprimir mensaje
  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, longitud
  int 0x80

  ; Calcular longitud del numero ya convertido
  inc edi                         ; EDI apunta al primer digito
  mov ecx, edi                    ; Puntero al primer digito
  mov esi, buffer + 11            ; Puntero al final del buffer
  sub esi, edi                    ; ESI = longitud del numero + LF

  ; Imprimir numero
  mov eax, 4
  mov ebx, 1
  mov edx, esi
  int 0x80

  ; Salir
  mov eax, 1
  xor ebx, ebx
  int 0x80
