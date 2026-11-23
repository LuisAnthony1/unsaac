; ============================================================================
; UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
; DEPARTAMENTO ACADÉMICO DE INGENIERÍA INFORMÁTICA
; ORGANIZACIÓN Y ARQUITECTURA DEL COMPUTADOR
;
; LABORATORIO 08: EJERCICIOS PROPUESTOS EN LENGUAJE ENSAMBLADOR (x86 32-bits)
; Programa      : Lab08_Palindromo_32.asm
; Autor         : Luis Anthony Mamani Mescco (Código: 194522)
; Docente       : Mgt. Manuel Aurelio Peñaloza Figueroa (Leunam)
; Semestre      : 2026-II
;
; COMPILACIÓN Y ENLAZADO (Linux x86 32-bits):
;   $ nasm -f elf32 Lab08_Palindromo_32.asm -o Lab08_Palindromo_32.o
;   $ ld -m elf_i386 Lab08_Palindromo_32.o -o Lab08_Palindromo_32
;   $ ./Lab08_Palindromo_32
; ============================================================================

MAX_CHARS equ 40

section .data
  msj_titulo   db 10, "============================================================", 10
               db " UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO", 10
               db " DEPARTAMENTO ACADEMICO DE INGENIERIA INFORMATICA", 10
               db " ORGANIZACION Y ARQUITECTURA DEL COMPUTADOR - LAB 08 (32-bit)", 10
               db " DETECTOR DE PALINDROMOS EN LENGUAJE ENSAMBLADOR NASM", 10
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

section .bss
  buf_input    resb 128
  buf_clean    resb 128
  buf_rev      resb 128
  buf_num      resb 32
  input_len    resd 1
  clean_len    resd 1

section .text
  global _start

_start:
  ; 1. Encabezado
  mov edx, msj_titulo
  call imprimir_string

  ; 2. Prompt
  mov edx, msj_prompt
  call imprimir_string

  ; 3. sys_read (eax = 3, ebx = 0 stdin, ecx = buf, edx = len)
  mov eax, 3
  mov ebx, 0
  mov ecx, buf_input
  mov edx, 128
  int 0x80

  cmp eax, 0
  jle .salir_vacia

  ; 4. Eliminar \n y \r finales
  mov ecx, eax
.strip_nl:
  cmp ecx, 0
  jle .salir_vacia
  mov al, [buf_input + ecx - 1]
  cmp al, 10
  je .quitar_char
  cmp al, 13
  je .quitar_char
  jmp .fin_strip

.quitar_char:
  mov byte [buf_input + ecx - 1], 0
  dec ecx
  jmp .strip_nl

.fin_strip:
  mov [input_len], ecx
  mov byte [buf_input + ecx], 0

  ; 5. Validar longitud
  cmp ecx, 0
  je .salir_vacia
  cmp ecx, MAX_CHARS
  jg .error_longitud

  ; 6. Procesar espacios y mayúsculas
  xor esi, esi
  xor edi, edi

.loop_filtro:
  cmp esi, [input_len]
  jge .fin_filtro

  mov al, [buf_input + esi]
  inc esi

  cmp al, ' '
  je .loop_filtro
  cmp al, 9
  je .loop_filtro

  cmp al, 'A'
  jl .guardar_limpio
  cmp al, 'Z'
  jg .guardar_limpio
  add al, 32

.guardar_limpio:
  mov [buf_clean + edi], al
  inc edi
  jmp .loop_filtro

.fin_filtro:
  mov [clean_len], edi
  mov byte [buf_clean + edi], 0

  cmp edi, 0
  je .salir_solo_espacios

  ; 7. Cadena invertida
  mov ecx, [clean_len]
  xor esi, esi

.loop_invertir:
  cmp esi, ecx
  jge .fin_invertir
  mov edx, ecx
  sub edx, 1
  sub edx, esi
  mov al, [buf_clean + edx]
  mov [buf_rev + esi], al
  inc esi
  jmp .loop_invertir

.fin_invertir:
  mov byte [buf_rev + ecx], 0

  ; 8. Mostrar detalles
  mov edx, msj_detalle
  call imprimir_string

  mov edx, msj_orig
  call imprimir_string
  mov edx, buf_input
  call imprimir_string
  mov edx, msj_comillas
  call imprimir_string

  mov edx, msj_orig_len
  call imprimir_string
  mov eax, [input_len]
  call imprimir_numero
  mov edx, msj_caracter
  call imprimir_string

  mov edx, msj_proc
  call imprimir_string
  mov edx, buf_clean
  call imprimir_string
  mov edx, msj_proc_exp
  call imprimir_string

  mov edx, msj_proc_len
  call imprimir_string
  mov eax, [clean_len]
  call imprimir_numero
  mov edx, msj_caracter
  call imprimir_string

  mov edx, msj_inv
  call imprimir_string
  mov edx, buf_rev
  call imprimir_string
  mov edx, msj_comillas
  call imprimir_string

  ; 9. Comparación dos punteros
  mov esi, buf_clean
  mov edx, [clean_len]
  lea edi, [buf_clean + edx - 1]

.loop_comparar:
  cmp esi, edi
  jge .es_palindromo

  mov al, [esi]
  mov bl, [edi]
  cmp al, bl
  jne .no_es_palindromo

  inc esi
  dec edi
  jmp .loop_comparar

.es_palindromo:
  mov edx, msj_linea
  call imprimir_string
  mov edx, msj_dictamen
  call imprimir_string
  mov edx, msj_es_pal
  call imprimir_string
  mov edx, msj_pie
  call imprimir_string

  mov eax, 1                              ; sys_exit
  xor ebx, ebx
  int 0x80

.no_es_palindromo:
  mov edx, msj_linea
  call imprimir_string
  mov edx, msj_dictamen
  call imprimir_string
  mov edx, msj_no_pal
  call imprimir_string
  mov edx, msj_pie
  call imprimir_string

  mov eax, 1                              ; sys_exit
  xor ebx, ebx
  int 0x80

.error_longitud:
  mov edx, msj_err_len
  call imprimir_string
  mov eax, [input_len]
  call imprimir_numero
  mov edx, msj_err_len2
  call imprimir_string
  mov eax, 1
  mov ebx, 1
  int 0x80

.salir_vacia:
  mov edx, msj_err_vacia
  call imprimir_string
  mov eax, 1
  xor ebx, ebx
  int 0x80

.salir_solo_espacios:
  mov edx, msj_err_esp
  call imprimir_string
  mov eax, 1
  xor ebx, ebx
  int 0x80

; --- Subrutinas auxiliares 32 bits ---
strlen:
  xor eax, eax
.loop_len:
  cmp byte [edx + eax], 0
  je .fin_len
  inc eax
  jmp .loop_len
.fin_len:
  ret

imprimir_string:
  push eax
  push ebx
  push ecx
  push edx
  call strlen
  mov ecx, edx                            ; ECX = buffer
  mov edx, eax                            ; EDX = longitud
  mov eax, 4                              ; sys_write
  mov ebx, 1                              ; stdout
  int 0x80
  pop edx
  pop ecx
  pop ebx
  pop eax
  ret

imprimir_numero:
  push eax
  push ebx
  push ecx
  push edx
  push esi

  lea esi, [buf_num + 31]
  mov byte [esi], 0
  mov ebx, 10
  xor ecx, ecx

  test eax, eax
  jnz .conv
  dec esi
  mov byte [esi], '0'
  mov ecx, 1
  jmp .imp

.conv:
  xor edx, edx
  div ebx
  add dl, '0'
  dec esi
  mov [esi], dl
  inc ecx
  test eax, eax
  jnz .conv

.imp:
  mov eax, 4
  mov ebx, 1
  mov edx, ecx
  mov ecx, esi
  int 0x80

  pop esi
  pop edx
  pop ecx
  pop ebx
  pop eax
  ret
