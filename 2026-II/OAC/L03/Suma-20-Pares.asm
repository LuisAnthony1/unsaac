; Programa: Suma-20-Pares.asm
;
; Descripcion: Suma los primeros 20 numeros pares (2+4+6+...+40 = 420),
;              usando TEST para verificar la paridad de cada candidato.
;              Luego convierte el resultado a cadena ASCII y lo imprime.
;
; Compilacion: nasm -f elf Suma-20-Pares.asm -o Suma-20-Pares.o
; Linkeado:    ld -m elf_i386 Suma-20-Pares.o -o Suma-20-Pares
; Ejecucion:   ./Suma-20-Pares

section .data
  msj db "La suma de los primeros 20 numeros pares es: "
  longitud equ $ - msj

section .bss
  buffer resb 12            ; buffer para el numero convertido a cadena

section .text
  global _start

_start:
  mov ecx, 20                ; contador de pares que faltan por sumar
  mov ebx, 0                 ; numero candidato
  mov eax, 0                 ; acumulador (suma)

ciclo:
  inc ebx
  test ebx, 1                ; ZF=1 si ebx es par (bit0 = 0)
  jnz ciclo                  ; si es impar, probar el siguiente candidato

  add eax, ebx                ; es par: sumarlo al acumulador
  loop ciclo                   ; ECX -= 1 y repite si ECX != 0

fin:
  mov esi, eax                ; preservar la suma en ESI (EAX se reutiliza)

  ; Imprimir el mensaje
  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, longitud
  int 0x80

  ; --- Convertir la suma (en ESI) a cadena ASCII ---
  mov edi, buffer + 11         ; apuntar al final del buffer
  mov byte [edi], 10            ; caracter de nueva linea al final
  mov ebx, 10                    ; divisor = 10 (base 10)
  mov eax, esi                    ; EAX = numero a convertir

.convertir:
  dec edi
  xor edx, edx                ; EDX = 0 (pre-condicion para la division)
  div ebx                      ; EAX = EAX/10, EDX = EAX%10
  add dl, '0'                   ; convertir el digito a ASCII
  mov [edi], dl                  ; guardarlo en el buffer
  test eax, eax                   ; ¿EAX == 0?
  jnz .convertir                   ; si no, seguir convirtiendo

.imprimir:
  mov esi, buffer + 11          ; puntero al final del buffer
  sub esi, edi                   ; ESI = ESI - EDI
  inc esi                         ; +1 porque EDI quedo apuntando al 1er
                                   ; digito (longitud real = diferencia + 1)

  mov eax, 4
  mov ebx, 1
  lea ecx, [edi]
  mov edx, esi
  int 0x80

  ; Salir
  mov eax, 1
  xor ebx, ebx
  int 0x80
