; Programa: Arreglo-Suma-de-Elementos.asm
;
; Compilacion: nasm -f elf Arreglo-Suma-de-Elementos.asm -o Arreglo-Suma-de-Elementos.o
;   Linkeado:  ld -m elf_i386 Arreglo-Suma-de-Elementos.o -o Arreglo-Suma-de-Elementos
;   Ejecucion: ./Arreglo-Suma-de-Elementos

section .data
  arreglo dd 100, 200, 300, 400     ; Arreglo de dwords (DD = 4 Bytes)
  len equ ($ - arreglo)/4             ; Longitud del arreglo (en # de elementos)
                                        ; (4 Bytes por elemento)
  suma dd 0                              ; suma = 0
  msj_suma db "Suma: ", 0xA                ; Mensaje
  len_msj_suma equ ($ - msj_suma)

section .bss
  str_suma resb 10                          ; Buffer para la suma (hasta 10 digitos)

section .text
  global _start

_start:
  ; Calcular suma
  mov esi, 0
  mov ecx, len
  mov ebx, 0                                  ; Acumulador

sumar:
  add ebx, [arreglo + esi*4]                    ; EBX = EBX + Elemento (DD = dword)
  inc esi
  loop sumar

  mov [suma], ebx                                ; Guardar resultado

  ; Convertir suma a ASCII
  mov eax, ebx                                    ; EAX = EBX
  mov edi, str_suma + 9                             ; Ultima posicion del buffer
  mov byte [edi], 0xA                                ; NL al final

  dec edi                                              ; EDI = EDI - 1

  mov ecx, 10                                           ; Divisor = ECX = 10

convertir:
  xor edx, edx                                            ; Inicializar EDX (EDX = 0)
  div ecx                                                  ; Cociente: EAX = EDX:EAX DIV ECX
                                                              ; Resto: EDX = EDX:EAX MOD ECX

  add dl, '0'                                                ; Convertir resto a ASCII
  mov [edi], dl                                                ; Almacenar digito en buffer
  dec edi                                                        ; Mover el puntero a la anterior posicion
  test eax, eax                                                    ; ¿Cociente = 0?
  jnz convertir

  ; Imprimir "Suma: "
  mov eax, 4                                                         ; sys_write
  mov ebx, 1                                                           ; stdout
  mov ecx, msj_suma                                                      ; direccion/puntero de "mensaje"
  mov edx, len_msj_suma                                                    ; longitud de "mensaje"
  int 0x80

  ; Imprimir valor de la suma
  inc edi                                                                   ; Ajustar al primer digito valido
  mov ecx, edi                                                                ; Direccion inicial de los digitos
  mov edx, str_suma + 10                                                       ; Fin del buffer
  sub edx, edi                                                                   ; Calcular longitud (edx = fin - inicio)
  mov eax, 4                                                                      ; sys_write
  int 0x80

  ; Salir
  mov eax, 1                                                                         ; sys_exit
  int 0x80
