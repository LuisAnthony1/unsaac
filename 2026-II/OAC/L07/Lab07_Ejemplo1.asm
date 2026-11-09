; Programa: Lab07_Ejemplo1.asm
; Compilación: ~$ nasm -f elf64 Lab07_Ejemplo1.asm
;      Linkeado: ~$ ld Lab07_Ejemplo1.o -o Lab07_Ejemplo1
;     Ejecución: ~$ ./Lab07_Ejemplo1

section .data
  msj_entrada1 db "Ingrese el 1er numero: ", 0
  msj_entrada2 db "Ingrese el 2do numero: ", 0
  msj_mul      db "Multiplicacion: ", 0
  msj_div_ent  db "Division entera: ", 0
  msj_mod      db "Modulo: ", 0
  NL           db 10                      ; Salto de línea (Line Feed)
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
  lea rdi, [msj_entrada1]                 ; RDI = puntero a msj_entrada1
  call imprimir_string
  call leer_entero
  mov [num1], rax

  ; 2. Leer 2do número
  lea rdi, [msj_entrada2]                 ; RDI = puntero a msj_entrada2
  call imprimir_string
  call leer_entero
  mov [num2], rax

  ; 3. Multiplicación (con signo: IMUL)
  mov rax, [num1]                         ; RAX = num1
  mov rbx, [num2]                         ; RBX = num2
  imul rax, rbx                           ; RAX = RAX * RBX
  mov rsi, rax                            ; RSI = producto
  lea rdi, [buffer]                       ; RDI = buffer de conversión
  call int_to_str
  lea rsi, [buffer]                       ; RSI = cadena formateada
  lea rdi, [msj_mul]                      ; RDI = mensaje de multiplicación
  call imprimir_resultado

  ; 4. División entera (con signo: IDIV con extensión de signo CQO)
  mov rax, [num1]
  cqo                                     ; RDX:RAX = extensión de signo de RAX
  mov rbx, [num2]
  idiv rbx                                ; RAX = cociente, RDX = residuo
  mov rsi, rax                            ; RSI = cociente
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_div_ent]
  call imprimir_resultado

  ; 5. Módulo / Residuo (RDX tras IDIV)
  mov rax, [num1]
  cqo
  mov rbx, [num2]
  idiv rbx                                ; RDX = residuo (preserva el signo del dividendo)
  mov rsi, rdx                            ; RSI = residuo
  lea rdi, [buffer]
  call int_to_str
  lea rsi, [buffer]
  lea rdi, [msj_mod]
  call imprimir_resultado

  ; 6. Terminar ejecución limpia (sys_exit = 60)
  mov rax, 60                             ; sys_exit
  xor rdi, rdi                            ; código de salida = 0
  syscall

; ----------------------------------------------------------------------------
; Subrutina: imprimir_resultado
; Entradas : RDI = puntero a cadena del mensaje descriptivo
;            RSI = puntero a cadena del valor numérico
; ----------------------------------------------------------------------------
imprimir_resultado:
  push rsi                                ; Guardar puntero al valor en la pila
  push rdi                                ; Guardar puntero al mensaje en la pila

  ; Imprimir mensaje descriptivo
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; fd: stdout = 1
  pop rsi                                 ; RSI = puntero al mensaje
  call strlen                             ; RAX = longitud del mensaje
  mov rdx, rax                            ; RDX = número de bytes a escribir
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; fd: stdout = 1
  syscall

  ; Imprimir valor formateado
  pop rsi                                 ; RSI = puntero al buffer del valor
  call strlen                             ; RAX = longitud del valor
  mov rdx, rax                            ; RDX = bytes a escribir
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; fd: stdout = 1
  syscall

  ; Imprimir salto de línea
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; fd: stdout = 1
  lea rsi, [NL]                           ; puntero a salto de línea
  mov rdx, 1                              ; 1 byte
  syscall

  ret

; ----------------------------------------------------------------------------
; Subrutina: imprimir_string
; Entrada  : RDI = puntero a cadena terminada en NUL
; ----------------------------------------------------------------------------
imprimir_string:
  mov rsi, rdi                            ; RSI = puntero a la cadena
  call strlen                             ; RAX = longitud
  mov rdx, rax                            ; RDX = longitud en bytes
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; fd: stdout = 1
  syscall

  ret

; ----------------------------------------------------------------------------
; Subrutina: strlen
; Entrada  : RSI = puntero a cadena terminada en NUL
; Salida   : RAX = número de caracteres (sin incluir el NUL)
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
; Salida   : RAX = número entero con signo leído desde stdin
; ----------------------------------------------------------------------------
leer_entero:
  mov rax, 0                              ; sys_read
  mov rdi, 0                              ; fd: stdin = 0
  lea rsi, [buffer]                       ; RSI = buffer de entrada
  mov rdx, 64                             ; máximo 64 bytes a leer
  syscall

  ; Convertir cadena ASCII leída a entero con signo de 64 bits
  lea rsi, [buffer]
  call str_to_int
  ret

; ----------------------------------------------------------------------------
; Subrutina: str_to_int
; Entrada  : RSI = puntero a cadena ASCII (acepta prefijo '-' opcional y newline)
; Salida   : RAX = entero con signo de 64 bits
; ----------------------------------------------------------------------------
str_to_int:
  xor rax, rax                            ; Acumulador numérico
  xor rbx, rbx                            ; Registro de dígito
  xor rdx, rdx                            ; Indicador de signo (0 = positivo, 1 = negativo)
  mov bl, [rsi]
  cmp bl, '-'                             ; ¿Comienza con signo negativo?
  jne .parse

  inc rsi                                 ; Avanzar más allá del signo '-'
  mov dl, 1                               ; Marcar como negativo

.parse:
  mov bl, [rsi]
  cmp bl, 10                              ; Salto de línea (\n) marca fin de entrada
  je .done
  cmp bl, 0                               ; NUL marca fin de cadena
  je .done

  sub bl, '0'                             ; Convertir carácter ASCII a dígito binario (0-9)
  imul rax, 10                            ; Multiplicar acumulador por 10
  add rax, rbx                            ; Sumar nuevo dígito
  inc rsi                                 ; Avanzar al siguiente carácter
  jmp .parse

.done:
  cmp dl, 1                               ; Si era negativo, aplicar negación en Complemento a 2
  jne .exit
  neg rax

.exit:
  ret

; ----------------------------------------------------------------------------
; Subrutina: int_to_str
; Entrada  : RSI = entero con signo de 64 bits
;            RDI = puntero a buffer de destino
; Salida   : Cadena ASCII terminada en NUL en el buffer destino
; ----------------------------------------------------------------------------
int_to_str:
  mov rax, rsi
  cmp rsi, 0                              ; Verificar si el número es negativo
  jge .convertir

  neg rsi                                 ; Negar para obtener el valor absoluto
  mov al, '-'
  stosb                                   ; Escribir '-' y avanzar RDI

.convertir:
  mov rax, rsi
  mov rcx, 0                              ; Contador de dígitos generados

.loop:
  xor rdx, rdx                            ; Limpiar RDX para división de 64 bits
  mov rbx, 10
  div rbx                                 ; RAX = cociente, RDX = residuo (dígito)
  push rdx                                ; Apilar el dígito
  inc rcx                                 ; Incrementar contador de dígitos
  test rax, rax                           ; ¿Quedan dígitos por extraer?
  jnz .loop

.print_digitos:
  pop rdx                                 ; Desapilar dígito en orden correcto
  add dl, '0'                             ; Convertir dígito binario a carácter ASCII
  mov [rdi], dl
  inc rdi
  loop .print_digitos

  mov byte [rdi], 0                       ; Terminador NUL
  ret

; Declarar sección de pila no ejecutable (buena práctica de seguridad ELF)
section .note.GNU-stack noalloc noexec nowrite progbits

