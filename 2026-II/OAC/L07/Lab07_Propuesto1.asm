; Programa: Lab07_Propuesto1.asm
; Compilación: ~$ nasm -f elf64 Lab07_Propuesto1.asm
;      Linkeado: ~$ ld Lab07_Propuesto1.o -o Lab07_Propuesto1
;     Ejecución: ~$ ./Lab07_Propuesto1

section .data
  msj_entrada1 db "Ingrese el 1er numero: ", 0
  msj_entrada2 db "Ingrese el 2do numero: ", 0
  msj_mul      db "Multiplicacion: ", 0
  msj_div_ent  db "Division entera: ", 0
  msj_mod      db "Modulo: ", 0
  msj_div_dec  db "Division decimal (4 decimales): ", 0
  msj_ovf_mul  db "Multiplicacion: desbordamiento (no cabe en 64 bits)", 10, 0
  msj_err_cero db "Error: division por cero.", 10, 0
  msj_err_ovf  db "Error: desbordamiento en la division (-2^63 / -1).", 10, 0
  msj_ovf_dec  db "Division decimal: desbordamiento al escalar el dividendo", 10, 0
  NL           db 10                      ; Salto de línea
  buffer       times 64 db 0

section .bss
  num1 resq 1                             ; Primer operando (64 bits)
  num2 resq 1                             ; Segundo operando (64 bits)

section .text
  global _start

; ----------------------------------------------------------------------------
; Punto de entrada principal
; ----------------------------------------------------------------------------
_start:
  ; 1. Leer 1er número
  lea rdi, [msj_entrada1]
  call imprimir_string
  call leer_entero
  mov [num1], rax

  ; 2. Leer 2do número
  lea rdi, [msj_entrada2]
  call imprimir_string
  call leer_entero
  mov [num2], rax

  ; 3. Multiplicación (con detección de desbordamiento mediante flag OF)
  mov rax, [num1]
  mov rbx, [num2]
  imul rax, rbx
  jo .mul_ovf                             ; Salta si el producto desborda 64 bits
  mov rsi, rax
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_mul]
  call imprimir_resultado
  jmp .validar

.mul_ovf:
  lea rdi, [msj_ovf_mul]
  call imprimir_string

.validar:
  ; 4. Validar divisor distinto de cero (previene SIGFPE)
  cmp qword [num2], 0
  jne .chk_critico
  lea rdi, [msj_err_cero]
  call imprimir_string
  jmp .salir_error

.chk_critico:
  ; Validar caso límite crítico: -2^63 / -1 (provoca desbordamiento en 64 bits)
  mov rax, 0x8000000000000000
  cmp [num1], rax
  jne .division
  cmp qword [num2], -1
  jne .division
  lea rdi, [msj_err_ovf]
  call imprimir_string
  jmp .salir_error

.division:
  ; 5. División entera
  mov rax, [num1]
  cqo                                     ; RDX:RAX = extensión de signo de RAX
  mov rbx, [num2]
  idiv rbx                                ; RAX = cociente, RDX = residuo
  mov rsi, rax
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_div_ent]
  call imprimir_resultado

  ; 6. Módulo / Residuo
  mov rax, [num1]
  cqo
  mov rbx, [num2]
  idiv rbx                                ; RDX = residuo (preserva signo del dividendo)
  mov rsi, rdx
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_mod]
  call imprimir_resultado

  ; 7. División decimal con 4 decimales mediante escalado x 10^4
  mov rax, [num1]
  imul rax, 10000                         ; RAX = num1 * 10000
  jo .dec_ovf                             ; Verificar desbordamiento al escalar
  cqo
  mov rbx, [num2]
  idiv rbx                                ; RAX = cociente escalado (con signo)

  lea rdi, [buffer]                       ; RDI = destino de la cadena
  test rax, rax
  jns .dec_positivo
  neg rax                                 ; Convertir a valor absoluto para formatear
  mov byte [rdi], '-'                     ; Prefijar signo negativo
  inc rdi

.dec_positivo:
  xor rdx, rdx
  mov rcx, 10000
  div rcx                                 ; RAX = parte entera, RDX = fracción (0..9999)
  push rdx                                ; Preservar fracción
  mov rsi, rax
  call uint_to_str                        ; Escribe parte entera (RDI queda en el NUL)
  mov byte [rdi], '.'                     ; Punto decimal
  inc rdi
  pop rax                                 ; RAX = parte fraccionaria
  mov rcx, 4                              ; Formatear con exactamente 4 dígitos
  call frac_to_str                        ; Escribe fracción rellenando ceros a la izquierda
  lea rsi, [buffer]
  lea rdi, [msj_div_dec]
  call imprimir_resultado

  ; Salida exitosa (código 0)
  xor rdi, rdi
.salir:
  mov rax, 60                             ; sys_exit
  syscall

.dec_ovf:
  lea rdi, [msj_ovf_dec]
  call imprimir_string

.salir_error:
  mov rdi, 1                              ; código de error = 1
  jmp .salir

; ----------------------------------------------------------------------------
; Subrutina: imprimir_resultado
; Entradas : RDI = puntero a mensaje
;            RSI = puntero a valor numérico
; ----------------------------------------------------------------------------
imprimir_resultado:
  push rsi
  push rdi

  ; Imprimir etiqueta
  mov rax, 1
  mov rdi, 1
  pop rsi
  call strlen
  mov rdx, rax
  mov rax, 1
  mov rdi, 1
  syscall

  ; Imprimir valor numérico
  pop rsi
  call strlen
  mov rdx, rax
  mov rax, 1
  mov rdi, 1
  syscall

  ; Imprimir salto de línea
  mov rax, 1
  mov rdi, 1
  lea rsi, [NL]
  mov rdx, 1
  syscall

  ret

; ----------------------------------------------------------------------------
; Subrutina: imprimir_string
; Entrada  : RDI = puntero a cadena
; ----------------------------------------------------------------------------
imprimir_string:
  mov rsi, rdi
  call strlen
  mov rdx, rax
  mov rax, 1
  mov rdi, 1
  syscall

  ret

; ----------------------------------------------------------------------------
; Subrutina: strlen
; Entrada  : RSI = puntero a cadena
; Salida   : RAX = longitud
; ----------------------------------------------------------------------------
strlen:
  xor rax, rax

.loop:
  cmp byte [rsi + rax], 0
  je .done
  inc rax
  jmp .loop

.done:
  ret

; ----------------------------------------------------------------------------
; Subrutina: leer_entero
; Salida   : RAX = entero leído desde stdin
; ----------------------------------------------------------------------------
leer_entero:
  mov rax, 0                              ; sys_read
  mov rdi, 0                              ; fd: stdin
  lea rsi, [buffer]
  mov rdx, 64
  syscall

  lea rsi, [buffer]
  call str_to_int
  ret

; ----------------------------------------------------------------------------
; Subrutina: str_to_int
; Entrada  : RSI = puntero a cadena ASCII
; Salida   : RAX = entero de 64 bits con signo
; ----------------------------------------------------------------------------
str_to_int:
  xor rax, rax
  xor rbx, rbx
  xor rdx, rdx
  mov bl, [rsi]
  cmp bl, '-'
  jne .parse

  inc rsi
  mov dl, 1                               ; Bandera de signo negativo

.parse:
  mov bl, [rsi]
  cmp bl, 10
  je .done
  cmp bl, 0
  je .done

  sub bl, '0'
  imul rax, 10
  add rax, rbx
  inc rsi
  jmp .parse

.done:
  cmp dl, 1
  jne .exit
  neg rax

.exit:
  ret

; ----------------------------------------------------------------------------
; Subrutina: int_to_str
; Entrada  : RSI = número con signo
;            RDI = buffer destino
; ----------------------------------------------------------------------------
int_to_str:
  mov rax, rsi
  cmp rsi, 0
  jge .convertir

  neg rsi
  mov al, '-'
  stosb

.convertir:
  mov rax, rsi
  mov rcx, 0

.loop:
  xor rdx, rdx
  mov rbx, 10
  div rbx
  push rdx
  inc rcx
  test rax, rax
  jnz .loop

.print_digitos:
  pop rdx
  add dl, '0'
  mov [rdi], dl
  inc rdi
  loop .print_digitos

  mov byte [rdi], 0
  ret

; ----------------------------------------------------------------------------
; Subrutina: uint_to_str (entero sin signo a cadena)
; Entrada  : RSI = valor sin signo
;            RDI = buffer de salida (al terminar, RDI apunta al byte NUL)
; ----------------------------------------------------------------------------
uint_to_str:
  mov rax, rsi
  xor rcx, rcx
  mov rbx, 10

.loop:
  xor rdx, rdx
  div rbx
  push rdx
  inc rcx
  test rax, rax
  jnz .loop

.print_digitos:
  pop rdx
  add dl, '0'
  mov [rdi], dl
  inc rdi
  loop .print_digitos

  mov byte [rdi], 0
  ret

; ----------------------------------------------------------------------------
; Subrutina: frac_to_str (formatea fracción con ceros a la izquierda)
; Entradas : RAX = valor numérico
;            RCX = número de posiciones decimales fijas
;            RDI = buffer destino (al terminar, RDI apunta al byte NUL)
; ----------------------------------------------------------------------------
frac_to_str:
  mov r8, rcx
  add rdi, r8
  mov byte [rdi], 0                       ; Terminador NUL al final
  mov rbx, 10

.loop:
  dec rdi
  xor rdx, rdx
  div rbx
  add dl, '0'
  mov [rdi], dl                           ; Escribir dígitos de derecha a izquierda
  dec rcx
  jnz .loop

  add rdi, r8                             ; Restaurar RDI a la posición del NUL final
  ret

; Pila no ejecutable
section .note.GNU-stack noalloc noexec nowrite progbits

