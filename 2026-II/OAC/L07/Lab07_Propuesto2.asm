; Programa: Lab07_Propuesto2.asm
; Compilación: ~$ nasm -f elf64 Lab07_Propuesto2.asm
;      Linkeado: ~$ ld Lab07_Propuesto2.o -o Lab07_Propuesto2
;     Ejecución: ~$ ./Lab07_Propuesto2

MAX_DEC equ 100                           ; Precisión máxima permitida (100 decimales)

section .data
  msj_entrada1 db "Ingrese el 1er numero: ", 0
  msj_entrada2 db "Ingrese el 2do numero: ", 0
  msj_entrada3 db "Ingrese el numero de decimales (0 a 100): ", 0
  msj_mul      db "Multiplicacion: ", 0
  msj_div_ent  db "Division entera: ", 0
  msj_mod      db "Modulo: ", 0
  msj_div_dec  db "Division decimal: ", 0
  msj_ovf_mul  db "Multiplicacion: desbordamiento (no cabe en 64 bits)", 10, 0
  msj_err_cero db "Error: division por cero.", 10, 0
  msj_err_ovf  db "Error: desbordamiento en la division (-2^63 / -1).", 10, 0
  msj_err_dec  db "Error: el numero de decimales debe estar entre 0 y 100.", 10, 0
  NL           db 10                      ; Salto de línea
  buffer       times 64 db 0

section .bss
  num1    resq 1                          ; Primer operando (64 bits)
  num2    resq 1                          ; Segundo operando (64 bits)
  ndec    resq 1                          ; Número de decimales solicitado
  buf_dec resb 160                        ; Buffer para resultado decimal largo

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

  ; 3. Leer y validar cantidad de decimales solicitados (0 .. MAX_DEC)
  lea rdi, [msj_entrada3]
  call imprimir_string
  call leer_entero
  cmp rax, 0
  jl .dec_invalido
  cmp rax, MAX_DEC
  jg .dec_invalido
  mov [ndec], rax

  ; 4. Multiplicación (con detección de overflow JO)
  mov rax, [num1]
  mov rbx, [num2]
  imul rax, rbx
  jo .mul_ovf                             ; Salta si excede 64 bits
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
  ; 5. Validar divisor distinto de cero (previene SIGFPE)
  cmp qword [num2], 0
  jne .chk_critico
  lea rdi, [msj_err_cero]
  call imprimir_string
  jmp .salir_error

.chk_critico:
  ; Validar caso límite crítico: -2^63 / -1
  mov rax, 0x8000000000000000
  cmp [num1], rax
  jne .division
  cmp qword [num2], -1
  jne .division
  lea rdi, [msj_err_ovf]
  call imprimir_string
  jmp .salir_error

.division:
  ; 6. División entera
  mov rax, [num1]
  cqo
  mov rbx, [num2]
  idiv rbx                                ; RAX = cociente, RDX = residuo
  mov rsi, rax
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_div_ent]
  call imprimir_resultado

  ; 7. Módulo / Residuo
  mov rax, [num1]
  cqo
  mov rbx, [num2]
  idiv rbx                                ; RDX = residuo con signo del dividendo
  mov rsi, rdx
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_mod]
  call imprimir_resultado

  ; 8. División decimal de precisión variable (algoritmo de división larga)
  mov rax, [num1]                         ; RAX = dividendo
  mov rbx, [num2]                         ; RBX = divisor
  mov rcx, [ndec]                         ; RCX = precisión de decimales
  lea rdi, [buf_dec]                      ; RDI = buffer de salida
  call division_decimal                   ; Retorna RDI = puntero al texto formateado
  mov rsi, rdi
  lea rdi, [msj_div_dec]
  call imprimir_resultado

  ; Salida limpia (código 0)
  xor rdi, rdi
.salir:
  mov rax, 60                             ; sys_exit
  syscall

.dec_invalido:
  lea rdi, [msj_err_dec]
  call imprimir_string

.salir_error:
  mov rdi, 1                              ; código de error = 1
  jmp .salir

; ----------------------------------------------------------------------------
; Subrutina: division_decimal
; Entradas : RAX = dividendo (con signo)
;            RBX = divisor (con signo, validado != 0)
;            RCX = cantidad de decimales requeridos
;            RDI = buffer de salida (>= 160 bytes)
; Salida   : RDI = puntero al inicio de la cadena resultante terminada en NUL
; Registros: R8  = contador de decimales pendientes
;            R9  = signo global (1 si dividend y divisor difieren de signo)
;            R10 = |divisor|
;            R11 = acumulador de magnitud (detecta si el resultado es != 0)
;            R12 = dirección base del buffer
;            R13 = residuo actual r
; ----------------------------------------------------------------------------
division_decimal:
  ; Calcular signo del resultado: bit 63 de (a XOR b) indica signos opuestos
  mov r9, rax
  xor r9, rbx
  shr r9, 63                              ; R9 = 1 si el cociente debe ser negativo

  ; Obtener valores absolutos sin signo (|a| y |b|)
  test rax, rax
  jns .a_ok
  neg rax
.a_ok:
  test rbx, rbx
  jns .b_ok
  neg rbx
.b_ok:
  mov r10, rbx                            ; R10 = |divisor|
  mov r8, rcx                             ; R8  = número de decimales
  mov r12, rdi                            ; Guardar posición base (reserva byte para '-')
  inc rdi                                 ; Comenzar a escribir en la posición 1

  ; Calcular parte entera = |a| / |b|
  xor rdx, rdx
  div r10                                 ; RAX = parte entera, RDX = resto inicial
  mov r13, rdx                            ; R13 = resto r
  mov r11, rax                            ; R11 acumula si algún dígito es distinto de 0
  mov rsi, rax
  call uint_to_str                        ; Escribe parte entera (RDI queda en el NUL)

  ; Si no se pidieron decimales, finalizar
  test r8, r8
  jz .signo
  mov byte [rdi], '.'                     ; Agregar punto decimal
  inc rdi

.dec_loop:
  test r8, r8
  jz .fin_dec

  ; Multiplicar resto por 10 usando aritmética de 128 bits (RDX:RAX = r * 10)
  mov rax, r13
  mov rcx, 10
  mul rcx                                 ; RDX:RAX = r * 10 (sin riesgo de overflow)
  div r10                                 ; RAX = nuevo dígito (0..9), RDX = nuevo resto
  mov r13, rdx
  or r11, rax                             ; Marcar si algún dígito fue != 0
  add al, '0'                             ; Convertir dígito a ASCII
  mov [rdi], al
  inc rdi
  dec r8
  jmp .dec_loop

.fin_dec:
  mov byte [rdi], 0                       ; Terminador NUL

.signo:
  ; El signo negativo '-' solo se incluye si el cociente es de signo opuesto
  ; Y el valor final no es estrictamente cero (evita mostrar "-0.000...")
  test r11, r11
  jz .sin_signo
  test r9, r9
  jz .sin_signo
  mov byte [r12], '-'
  mov rdi, r12                            ; Cadena inicia en el signo '-'
  ret

.sin_signo:
  lea rdi, [r12 + 1]                      ; Cadena inicia después del byte reservado
  ret

; ----------------------------------------------------------------------------
; Subrutina: imprimir_resultado
; Entradas : RDI = puntero a mensaje
;            RSI = puntero a cadena del valor numérico
; ----------------------------------------------------------------------------
imprimir_resultado:
  push rsi
  push rdi

  ; Imprimir mensaje descriptivo
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
  mov dl, 1

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
; Entrada  : RSI = entero con signo
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

; Pila no ejecutable
section .note.GNU-stack noalloc noexec nowrite progbits

