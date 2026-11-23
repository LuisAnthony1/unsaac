; ============================================================================
; UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
; DEPARTAMENTO ACADÉMICO DE INGENIERÍA INFORMÁTICA
; ORGANIZACIÓN Y ARQUITECTURA DEL COMPUTADOR
;
; LABORATORIO 08: EJERCICIOS PROPUESTOS EN LENGUAJE ENSAMBLADOR (x86-64)
; Programa      : Lab08_Palindromo.asm
; Autor         : Luis Anthony Mamani Mescco (Código: 194522)
; Docente       : Mgt. Manuel Aurelio Peñaloza Figueroa (Leunam)
; Semestre      : 2026-II
;
; OBJETIVO:
;   Leer una palabra o frase por consola de hasta 40 caracteres (letras,
;   dígitos, etc.), procesar los espacios omitiéndolos y normalizando
;   mayúsculas a minúsculas, e indicar si la palabra o frase es un PALÍNDROMO.
;
; COMPILACIÓN Y ENLAZADO (Linux x86-64):
;   $ nasm -f elf64 Lab08_Palindromo.asm -o Lab08_Palindromo.o
;   $ ld Lab08_Palindromo.o -o Lab08_Palindromo
;   $ ./Lab08_Palindromo
; ============================================================================

MAX_CHARS equ 40

section .data
  msj_titulo   db 10, "============================================================", 10
               db " UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO", 10
               db " DEPARTAMENTO ACADEMICO DE INGENIERIA INFORMATICA", 10
               db " ORGANIZACION Y ARQUITECTURA DEL COMPUTADOR - LAB 08", 10
               db " DETECTOR DE PALINDROMOS EN LENGUAJE ENSAMBLADOR NASM (x86-64)", 10
               db "============================================================", 10, 0

  msj_prompt   db 10, "Ingrese una palabra o frase (maximo 40 caracteres): ", 0

  msj_err_len  db 10, "[!] ERROR: La cadena ingresada excede los 40 caracteres permitidos.", 10
               db "    Longitud ingresada: ", 0
  msj_err_len2 db " caracteres. Maximo permitido: 40.", 10, 0

  msj_err_vacia db 10, "[!] AVISO: La cadena ingresada esta vacia.", 10, 0

  msj_err_esp   db 10, "[!] AVISO: La frase contiene unicamente espacios; no hay caracteres utiles.", 10, 0

  msj_detalle  db 10, "-------------------- DETALLE DEL ANALISIS --------------------", 10, 0
  msj_orig     db "[+] Cadena original    : \"", 0
  msj_orig_len db "[+] Longitud original  : ", 0
  msj_proc     db "[+] Cadena procesada   : \"", 0
  msj_proc_len db "[+] Longitud procesada : ", 0
  msj_proc_exp db "\" (espacios ignorados y minusculas)", 10, 0
  msj_inv      db "[+] Cadena invertida   : \"", 0
  msj_comillas db "\"", 10, 0
  msj_caracter db " caracteres", 10, 0

  msj_linea    db "--------------------------------------------------------------", 10, 0
  msj_dictamen db "DICTAMEN:", 10, 0
  msj_es_pal   db ">>> [EXITO] LA PALABRA O FRASE ES UN PALINDROMO <<<", 10, 0
  msj_no_pal   db ">>> [AVISO] LA PALABRA O FRASE NO ES UN PALINDROMO <<<", 10, 0
  msj_pie      db "==============================================================", 10, 10, 0

  NL           db 10, 0

section .bss
  buf_input    resb 128                   ; Buffer de entrada bruta
  buf_clean    resb 128                   ; Buffer sin espacios y normalizado
  buf_rev      resb 128                   ; Buffer invertido
  buf_num      resb 32                    ; Buffer temporal para imprimir números
  input_len    resq 1                     ; Longitud de la entrada original
  clean_len    resq 1                     ; Longitud de la cadena procesada

section .text
  global _start

; ----------------------------------------------------------------------------
; Punto de entrada principal
; ----------------------------------------------------------------------------
_start:
  ; 1. Imprimir encabezado del laboratorio
  lea rsi, [msj_titulo]
  call imprimir_string

  ; 2. Solicitar ingreso de datos
  lea rsi, [msj_prompt]
  call imprimir_string

  ; 3. Leer cadena desde la consola (sys_read = 0, stdin = 0)
  mov rax, 0                              ; sys_read
  mov rdi, 0                              ; stdin (fd = 0)
  lea rsi, [buf_input]                    ; puntero a buffer de lectura
  mov rdx, 128                            ; máximo de bytes a leer
  syscall

  ; Verificar si ocurrió error de lectura o EOF
  cmp rax, 0
  jle .salir_vacia

  ; 4. Eliminar saltos de línea finales (\n = 10, \r = 13)
  mov rcx, rax                            ; RCX = número de bytes leídos
.strip_nl:
  cmp rcx, 0
  jle .salir_vacia
  mov al, [buf_input + rcx - 1]
  cmp al, 10                              ; Salto de línea (\n)
  je .quitar_char
  cmp al, 13                              ; Retorno de carro (\r)
  je .quitar_char
  jmp .fin_strip

.quitar_char:
  mov byte [buf_input + rcx - 1], 0
  dec rcx
  jmp .strip_nl

.fin_strip:
  mov [input_len], rcx
  mov byte [buf_input + rcx], 0           ; Asegurar terminador nulo

  ; 5. Validar longitud de la entrada
  cmp rcx, 0
  je .salir_vacia

  cmp rcx, MAX_CHARS
  jg .error_longitud

  ; 6. Procesar espacios y convertir mayúsculas a minúsculas
  ;    RSI = índice de lectura en buf_input
  ;    RDI = índice de escritura en buf_clean
  xor rsi, rsi
  xor rdi, rdi

.loop_filtro:
  cmp rsi, [input_len]
  jge .fin_filtro

  mov al, [buf_input + rsi]
  inc rsi

  ; Omitir espacios (' ' = 32) y tabulaciones ('\t' = 9)
  cmp al, ' '
  je .loop_filtro
  cmp al, 9
  je .loop_filtro

  ; Normalizar letras mayúsculas a minúsculas ('A'-'Z' -> 'a'-'z')
  cmp al, 'A'
  jl .guardar_limpio
  cmp al, 'Z'
  jg .guardar_limpio
  add al, 32                              ; Convertir a minúscula (+32 en ASCII)

.guardar_limpio:
  mov [buf_clean + rdi], al
  inc rdi
  jmp .loop_filtro

.fin_filtro:
  mov [clean_len], rdi
  mov byte [buf_clean + rdi], 0           ; Asegurar terminador nulo

  ; 7. Validar si quedaron caracteres útiles tras remover espacios
  cmp rdi, 0
  je .salir_solo_espacios

  ; 8. Construir cadena invertida (buf_rev)
  ;    buf_rev[i] = buf_clean[clean_len - 1 - i]
  mov rcx, [clean_len]
  xor rsi, rsi

.loop_invertir:
  cmp rsi, rcx
  jge .fin_invertir

  mov rdx, rcx
  sub rdx, 1
  sub rdx, rsi
  mov al, [buf_clean + rdx]
  mov [buf_rev + rsi], al
  inc rsi
  jmp .loop_invertir

.fin_invertir:
  mov byte [buf_rev + rcx], 0             ; Asegurar terminador nulo

  ; 9. Mostrar detalle del procesamiento
  lea rsi, [msj_detalle]
  call imprimir_string

  ; Mostrar cadena original
  lea rsi, [msj_orig]
  call imprimir_string
  lea rsi, [buf_input]
  call imprimir_string
  lea rsi, [msj_comillas]
  call imprimir_string

  ; Mostrar longitud original
  lea rsi, [msj_orig_len]
  call imprimir_string
  mov rax, [input_len]
  call imprimir_numero
  lea rsi, [msj_caracter]
  call imprimir_string

  ; Mostrar cadena procesada
  lea rsi, [msj_proc]
  call imprimir_string
  lea rsi, [buf_clean]
  call imprimir_string
  lea rsi, [msj_proc_exp]
  call imprimir_string

  ; Mostrar longitud procesada
  lea rsi, [msj_proc_len]
  call imprimir_string
  mov rax, [clean_len]
  call imprimir_numero
  lea rsi, [msj_caracter]
  call imprimir_string

  ; Mostrar cadena invertida
  lea rsi, [msj_inv]
  call imprimir_string
  lea rsi, [buf_rev]
  call imprimir_string
  lea rsi, [msj_comillas]
  call imprimir_string

  ; 10. Algoritmo de verificación de Palíndromo (Dos Punteros)
  ;     RSI apunta al primer carácter de buf_clean
  ;     RDI apunta al último carácter de buf_clean
  lea rsi, [buf_clean]
  mov rdx, [clean_len]
  lea rdi, [buf_clean + rdx - 1]

.loop_comparar:
  cmp rsi, rdi
  jge .es_palindromo                      ; Punteros se cruzaron: todos coincidieron

  mov al, [rsi]
  mov bl, [rdi]
  cmp al, bl
  jne .no_es_palindromo                   ; Discrepancia encontrada

  inc rsi                                 ; Avanzar puntero izquierdo
  dec rdi                                 ; Retroceder puntero derecho
  jmp .loop_comparar

.es_palindromo:
  lea rsi, [msj_linea]
  call imprimir_string
  lea rsi, [msj_dictamen]
  call imprimir_string
  lea rsi, [msj_es_pal]
  call imprimir_string
  lea rsi, [msj_pie]
  call imprimir_string

  ; Salir con código 0
  mov rax, 60                             ; sys_exit
  xor rdi, rdi                            ; exit code = 0
  syscall

.no_es_palindromo:
  lea rsi, [msj_linea]
  call imprimir_string
  lea rsi, [msj_dictamen]
  call imprimir_string
  lea rsi, [msj_no_pal]
  call imprimir_string
  lea rsi, [msj_pie]
  call imprimir_string

  ; Salir con código 0
  mov rax, 60                             ; sys_exit
  xor rdi, rdi                            ; exit code = 0
  syscall

; --- Manejo de Casos Especiales y Errores ---
.error_longitud:
  lea rsi, [msj_err_len]
  call imprimir_string
  mov rax, [input_len]
  call imprimir_numero
  lea rsi, [msj_err_len2]
  call imprimir_string
  mov rax, 60                             ; sys_exit
  mov rdi, 1                              ; exit code = 1 (error de validación)
  syscall

.salir_vacia:
  lea rsi, [msj_err_vacia]
  call imprimir_string
  mov rax, 60                             ; sys_exit
  xor rdi, rdi
  syscall

.salir_solo_espacios:
  lea rsi, [msj_err_esp]
  call imprimir_string
  mov rax, 60                             ; sys_exit
  xor rdi, rdi
  syscall

; ============================================================================
; SUBRUTINAS AUXILIARES
; ============================================================================

; ----------------------------------------------------------------------------
; strlen: Calcula la longitud de una cadena terminada en nulo (0)
; Entrada : RSI = puntero a la cadena
; Salida  : RAX = número de caracteres
; ----------------------------------------------------------------------------
strlen:
  xor rax, rax
.loop_len:
  cmp byte [rsi + rax], 0
  je .fin_len
  inc rax
  jmp .loop_len
.fin_len:
  ret

; ----------------------------------------------------------------------------
; imprimir_string: Imprime por stdout una cadena terminada en nulo (0)
; Entrada : RSI = puntero a la cadena
; ----------------------------------------------------------------------------
imprimir_string:
  push rbx
  push rcx
  push rdx
  push rsi
  push rdi

  call strlen
  mov rdx, rax                            ; RDX = número de bytes
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; stdout (fd = 1)
  syscall

  pop rdi
  pop rsi
  pop rdx
  pop rcx
  pop rbx
  ret

; ----------------------------------------------------------------------------
; imprimir_numero: Convierte un entero de 64 bits a ASCII e imprime por stdout
; Entrada : RAX = valor entero sin signo a imprimir
; ----------------------------------------------------------------------------
imprimir_numero:
  push rbx
  push rcx
  push rdx
  push rsi
  push rdi
  push r8

  lea r8, [buf_num + 31]
  mov byte [r8], 0                        ; Terminador nulo al final
  mov rbx, 10                             ; Base decimal
  xor rcx, rcx                            ; Contador de caracteres

  test rax, rax
  jnz .convertir_digitos
  dec r8
  mov byte [r8], '0'
  mov rcx, 1
  jmp .imprimir_buffer

.convertir_digitos:
  xor rdx, rdx
  div rbx                                 ; RDX = residuo, RAX = cociente
  add dl, '0'
  dec r8
  mov [r8], dl
  inc rcx
  test rax, rax
  jnz .convertir_digitos

.imprimir_buffer:
  mov rax, 1                              ; sys_write
  mov rdi, 1                              ; stdout
  mov rsi, r8                             ; Puntero al inicio de los dígitos
  mov rdx, rcx                            ; Cantidad de bytes
  syscall

  pop r8
  pop rdi
  pop rsi
  pop rdx
  pop rcx
  pop rbx
  ret
