; Programa: Suma-nros-hasta-valor-negativo-01.asm
;
; Descripcion: Suma los valores de un arreglo de entrada hasta que se lea
;              un valor negativo (centinela), luego imprime la suma.
;
; Compilacion: nasm -f elf Suma-nros-hasta-valor-negativo-01.asm -o Suma-nros-hasta-valor-negativo-01.o
; Linkeado:    ld -m elf_i386 Suma-nros-hasta-valor-negativo-01.o -o Suma-nros-hasta-valor-negativo-01
; Ejecucion:   ./Suma-nros-hasta-valor-negativo-01

section .data
  entrada dd 5, 3, 16, -2, 4     ; Array de entrada (doble word)
  NL      db 10                  ; NL = caracter nueva linea

section .bss
  BUFFER  resb 12                ; Buffer para almacenar el string (del numero)

section .text
  global _start

_start:
  mov esi, entrada          ; Puntero al array
  mov eax, 0                 ; Acumulador (inicializar)

ciclo:
  mov ebx, [esi]              ; Cargar el elemento actual del Array
  cmp ebx, 0                   ; Realiza: EBX - 0
  jl fin                        ; Salir si es negativo

  add eax, ebx                   ; EAX = EAX + EBX (Sumar al acumulador)
  add esi, 4                      ; Apuntar al siguiente elemento (4 bytes = dd)
  jmp ciclo

fin:
  ; EAX contiene la suma. Convertir EAX a cadena ASCII:
  mov edi, BUFFER + 11        ; Apuntar al final del buffer
  mov byte [edi], '$'          ; caracter centinela (no se imprime)
  mov ebx, 10                   ; Divisor = 10 (base 10)

.convertir:
  dec edi                        ; Avanzar el puntero hacia atras

  xor edx, edx                    ; EDX = 0 (pre-condicion para la division)
  div ebx                          ; EAX = EAX/10 (cociente), EDX = EAX%10 (resto)

  add dl, '0'                        ; Convertir el digito a ASCII
  mov [edi], dl                       ; Guardarlo en el buffer
  test eax, eax                        ; ¿EAX == 0?
  jnz .convertir                        ; Si no, repetir

.imprimir:
  mov esi, BUFFER + 11                   ; Puntero al final del buffer
  sub esi, edi                            ; ESI = longitud de la cadena

  mov eax, 4                               ; sys_write
  mov ebx, 1
  lea ecx, [edi]                            ; inicio de la cadena
  mov edx, esi
  int 0x80

  mov eax, 4                               ; imprimir salto de linea
  mov ebx, 1
  mov ecx, NL
  mov edx, 1
  int 0x80

  mov eax, 1                               ; sys_exit
  xor ebx, ebx
  int 0x80
