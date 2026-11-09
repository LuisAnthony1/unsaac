; Programa: Arreglo-Recorrido-01.asm
;
; Compilacion: nasm -f elf Arreglo-Recorrido-01.asm -o Arreglo-Recorrido-01.o
;   Linkeado:  ld -m elf_i386 Arreglo-Recorrido-01.o -o Arreglo-Recorrido-01
;   Ejecucion: ./Arreglo-Recorrido-01

section .data
  arreglo db 5, 3, 9, 7, 1      ; Arreglo de bytes
  len equ ($ - arreglo)          ; Longitud del arreglo (en # de elementos)
  msj db "Elementos: ", 0xA       ; Mensaje inicial
  msj_len equ $ - msj              ; Longitud del mensaje

section .bss
  buffer resb 2                     ; Buffer para imprimir (2 Byte = digito + nuevalinea)

section .text
  global _start

_start:
  ; Imprimir mensaje "Elementos: "
  mov eax, 4
  mov ebx, 1
  mov ecx, msj
  mov edx, msj_len
  int 0x80

  ; Inicializar
  mov esi, 0             ; Indice inicial
  mov ecx, len             ; Contador del bucle = longitud del arreglo
                            ; (el valor actual de ECX se preservara)

recorrer_arreglo:
  ; Preservar ECX y ESI en la pila
  push ecx
  push esi

  ; Convertir byte a ASCII
  mov al, [arreglo + esi]   ; Cargar el elemento en AL
  add al, '0'                 ; Convertir a ASCII
  mov [buffer], al              ; Guardar elemento en buffer

  ; Imprimir el elemento
  mov eax, 4                      ; sys_write
  mov ebx, 1                        ; stdout
  mov ecx, buffer                     ; puntero/direccion de "buffer"
  mov edx, 1                            ; # de bytes a imprimir
  int 0x80

  ; Restaurar ECX y ESI desde la pila
  pop esi
  pop ecx

  inc esi                     ; Incrementar el indice
  loop recorrer_arreglo        ; Decrementar ECX y Repetir si ECX > 0

  ; Salir
  mov eax, 1
  ;xor ebx, ebx
  int 0x80
