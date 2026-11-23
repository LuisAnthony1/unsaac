# Laboratorio 08: Lenguaje Ensamblador — Ejercicios Propuestos (Detector de Palíndromos en x86-64)

**Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)**  
**Facultad de Ingeniería Eléctrica, Electrónica, Informática y Mecánica**  
**Departamento Académico de Ingeniería Informática**  
**Organización y Arquitectura del Computador (OAC)** — Semestre 2026-II  
**Docente:** Mgt. Manuel Aurelio Peñaloza Figueroa (*Leunam*)  
**Estudiante:** Luis Anthony Mamani Mescco (Código: 194522)  

---

## 1. Introducción y Objetivos

El presente laboratorio aborda el diseño e implementación de programas en **Lenguaje Ensamblador NASM puro** para la arquitectura **x86-64 (AMD64)** bajo sistemas operativos tipo Unix/Linux. El objetivo central es desarrollar un programa autónomo de alto rendimiento que resuelva el problema clásico de la **detección y validación de palíndromos** en cadenas alfanuméricas y frases complejas, comunicándose de forma directa con el kernel a través de llamadas al sistema (*syscalls*) sin depender de la biblioteca estándar de C (*libc*).

### Objetivos Específicos:
1. **Entrada y Salida en Ensamblador x86-64:** Gestionar buffers estáticos de memoria en la sección `.bss` para realizar lecturas por consola (`sys_read`, fd = 0) y escrituras formateadas (`sys_write`, fd = 1) mediante la instrucción `syscall`.
2. **Validación de Restricciones Operativas:** Controlar que la cadena leída cumpla estrictamente con el límite de longitud especificado en la guía ($\le 40$ caracteres), emitiendo avisos ante entradas vacías o que excedan dicho tamaño.
3. **Procesamiento de Espacios y Caracteres Especiales:** Diseñar un algoritmo de filtrado en bajo nivel que recorra byte a byte la entrada original, ignorando espacios en blanco (`' '` / ASCII 32) y tabuladores (`\t` / ASCII 9).
4. **Normalización de Caracteres (*Case-Folding*):** Implementar la transformación aritmética de letras mayúsculas (`'A'` - `'Z'`) a minúsculas (`'a'` - `'z'`) sumando 32 al código ASCII, permitiendo que frases como *"Anita lava la tina"* sean reconocidas con precisión matemática.
5. **Algoritmo de Dos Punteros:** Aplicar una estrategia de verificación bidireccional en tiempo lineal $O(N)$ utilizando registros puntero de 64 bits (`RSI` y `RDI`), comparando simétricamente los extremos hacia el centro.
6. **Entrega Completa de Artefactos:** Proporcionar el código fuente en ensamblador de 64 bits (`Lab08_Palindromo.asm`, `Lab08_Propuesto1.asm`), la versión compatible de 32 bits (`Lab08_Palindromo_32.asm`), automatización (`Makefile`, `build.sh`), simulador (`test_simulador.py`) y el informe técnico formal en PDF (`Lab 8 d OAC.pdf`).

---

## 2. Fundamentos Teóricos y Arquitectura x86-64

### 2.1. Definición y Tratamiento de Palíndromos en Lenguaje Natural
Un **palíndromo** es una palabra, número o frase que se lee idénticamente tanto de izquierda a derecha como de derecha a izquierda. En el ámbito informático y lingüístico, las frases en lenguaje natural presentan dos particularidades que deben ser procesadas:
1. **Espaciado y Puntuación:** Las palabras están separadas por espacios que no forman parte de la simetría fonética (ejemplo: *"dabale arroz a la zorra el abad"*). Por ende, el procesador debe omitir los espacios y compactar la cadena en un buffer limpio.
2. **Distinción de Caja (Mayúsculas vs Minúsculas):** En la tabla ASCII, la letra `'A'` (65 / 0x41) difiere a nivel binario de `'a'` (97 / 0x61). Sin normalización, una comparación directa indicaría falsamente que *"Radar"* o *"Anita"* no son palíndromos.

### 2.2. Aritmética de Normalización en la Tabla ASCII
En la codificación ASCII estándar:
- Las letras mayúsculas se ubican en el intervalo cerrado $[65, 90]$ (0x41 a 0x5A).
- Las letras minúsculas se ubican en el intervalo cerrado $[97, 122]$ (0x61 a 0x7A).
- La diferencia fija es de $97 - 65 = 32$ unidades (equivalente al bit 5 de un byte, `0x20`).

En ensamblador x86-64, la normalización condicional se implementa de forma óptima con instrucciones de comparación y suma de 8 bits:
```nasm
cmp al, 'A'
jl .no_es_mayuscula
cmp al, 'Z'
jg .no_es_mayuscula
add al, 32                  ; AL = AL + 32 (convierte mayúscula a minúscula)
.no_es_mayuscula:
```

### 2.3. Convención de Llamadas al Sistema (*System V AMD64 ABI*)
En Linux de 64 bits, la transición al espacio de núcleo (*kernel space*) se efectúa mediante la instrucción `syscall`. Los registros se distribuyen según el estándar:

| Parámetro | Registro x86-64 | Registro x86-32 (`int 0x80`) | Descripción |
| :--- | :---: | :---: | :--- |
| **Identificador de Syscall** | `RAX` | `EAX` | 0 = `sys_read`, 1 = `sys_write`, 60 = `sys_exit` |
| **Argumento 1 (File Descriptor)** | `RDI` | `EBX` | 0 = `stdin`, 1 = `stdout`, 2 = `stderr` |
| **Argumento 2 (Puntero a Buffer)** | `RSI` | `ECX` | Dirección de memoria en `.bss` o `.data` |
| **Argumento 3 (Longitud en Bytes)** | `RDX` | `EDX` | Número de bytes a transferir |
| **Valor de Retorno** | `RAX` | `EAX` | Bytes leídos/escritos o código de error |

> [!NOTE]
> La instrucción `syscall` modifica internamente los registros `RCX` y `R11`. Por ello, las subrutinas que involucren llamadas al sistema deben preservar cualquier valor crítico antes de su invocación.

### 2.4. Algoritmo de Verificación con Dos Punteros
El algoritmo opera sobre el buffer normalizado `buf_clean` de longitud $L$:
```
Puntero Izquierdo (RSI)                               Puntero Derecho (RDI)
         |                                                      |
         v                                                      v
       +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
       | a | n | i | t | a | l | a | v | a | l | a | t | i | n | a |
       +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
         0   1   2   3   4   5   6   7   8   9  10  11  12  13  14
```
1. `RSI = &buf_clean[0]`, `RDI = &buf_clean[L - 1]`.
2. Mientras `RSI < RDI`:
   - Comparar el byte `[RSI]` con `[RDI]`.
   - Si `[RSI] != [RDI]`, abortar: **NO ES PALÍNDROMO**.
   - Avanzar `RSI = RSI + 1`, retroceder `RDI = RDI - 1`.
3. Si los punteros se cruzan (`RSI >= RDI`), todos los caracteres coincidieron simétricamente: **ES UN PALÍNDROMO**.

---

## 3. Estructura y Archivos del Proyecto

La carpeta `L08/` contiene la solución íntegra con soporte multi-arquitectura:

```text
e:\Git\unsaac\2026-II\OAC\L08/
├── Lab08_Palindromo.asm       # Programa principal en x86-64 puro (NASM)
├── Lab08_Propuesto1.asm        # Archivo idéntico nombrado según convención oficial
├── Lab08_Palindromo_32.asm     # Versión alternativa de 32 bits (int 0x80)
├── Makefile                    # Reglas de compilación y limpieza automatizada
├── build.sh                    # Script bash para compilar y dar permisos
├── test_simulador.py           # Validador de los 15 casos de prueba en Python
├── generar_pdf.py              # Generador del informe técnico en PDF (ReportLab)
├── Lab 8 d OAC.pdf             # Informe digital oficial listo para entrega
├── Informe_Lab08_Palindromo.pdf# Copia con nomenclatura alternativa
├── README.md                   # Documentación técnica completa (este archivo)
└── L08-Lenguaje Ensamblador... # Guía oficial en PDF suministrada por el docente
```

---

## 4. Código Fuente Completo en Ensamblador (`Lab08_Palindromo.asm`)

```nasm
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
  mov rdi, 1                              ; exit code = 1 (error)
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
strlen:
  xor rax, rax
.loop_len:
  cmp byte [rsi + rax], 0
  je .fin_len
  inc rax
  jmp .loop_len
.fin_len:
  ret

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

imprimir_numero:
  push rbx
  push rcx
  push rdx
  push rsi
  push rdi
  push r8

  lea r8, [buf_num + 31]
  mov byte [r8], 0
  mov rbx, 10
  xor rcx, rcx

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
  mov rsi, r8                             ; Puntero a dígitos
  mov rdx, rcx                            ; Cantidad de bytes
  syscall

  pop r8
  pop rdi
  pop rsi
  pop rdx
  pop rcx
  pop rbx
  ret
```

---

## 5. Compilación, Enlazado y Ejecución

### Opción A: Compilación Directa con Comandos GNU/Linux
```bash
# 1. Ensamblar con NASM generando objeto ELF de 64 bits con depuración DWARF:
nasm -f elf64 -g -F dwarf Lab08_Palindromo.asm -o Lab08_Palindromo.o

# 2. Enlazar con GNU ld:
ld Lab08_Palindromo.o -o Lab08_Palindromo

# 3. Asignar permisos y ejecutar:
chmod +x Lab08_Palindromo
./Lab08_Palindromo
```

### Opción B: Utilizando el `Makefile` Automatizado
```bash
make          # Compila la versión de 64 bits (Lab08_Palindromo y Lab08_Propuesto1)
make 32       # Compila adicionalmente la versión de 32 bits (Lab08_Palindromo_32)
make run      # Ejecuta el programa principal
make clean    # Limpia archivos objetos (*.o) y binarios generados
```

### Opción C: Ejecutando el Script `build.sh`
```bash
bash build.sh
./Lab08_Palindromo
```

---

## 6. Casos de Prueba Verificados

| N° | Entrada de Prueba | Longitud Original | Cadena Procesada | Dictamen Emitido | Estado |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **01** | `"anita lava la tina"` | 18 | `anitalavalatina` | **ES UN PALÍNDROMO** | **APROBADO** |
| **02** | `"dabale arroz a la zorra el abad"` | 31 | `dabalearrozalazorraelabad` | **ES UN PALÍNDROMO** | **APROBADO** |
| **03** | `"reconocer"` | 9 | `reconocer` | **ES UN PALÍNDROMO** | **APROBADO** |
| **04** | `"somos o no somos"` | 16 | `somosonosomos` | **ES UN PALÍNDROMO** | **APROBADO** |
| **05** | `"radar"` | 5 | `radar` | **ES UN PALÍNDROMO** | **APROBADO** |
| **06** | `"12321"` | 5 | `12321` | **ES UN PALÍNDROMO** | **APROBADO** |
| **07** | `"123 43 21"` | 9 | `1234321` | **ES UN PALÍNDROMO** | **APROBADO** |
| **08** | `"A ti no bonita"` | 14 | `atinobonita` | **ES UN PALÍNDROMO** | **APROBADO** |
| **09** | `"oso"` | 3 | `oso` | **ES UN PALÍNDROMO** | **APROBADO** |
| **10** | `"Arquitectura de computadoras"` | 28 | `arquitecturadecomputadoras` | **NO ES UN PALÍNDROMO** | **APROBADO** |
| **11** | `"Hola mundo"` | 10 | `holamundo` | **NO ES UN PALÍNDROMO** | **APROBADO** |
| **12** | `"123456"` | 6 | `123456` | **NO ES UN PALÍNDROMO** | **APROBADO** |
| **13** | `""` (Línea vacía) | 0 | - | **AVISO: CADENA VACÍA** | **APROBADO** |
| **14** | `"      "` (Solo espacios) | 6 | - | **AVISO: SIN DATOS** | **APROBADO** |
| **15** | `"Frase con mas de cuarenta caracteres en total"` | 44 | - | **ERROR: > 40 CARACTERES** | **APROBADO** |

---

## 7. Preguntas Frecuentes y Depuración con GDB

### 1. ¿Cómo depurar paso a paso el bucle de dos punteros con GDB?
Dado que compilamos con `-g -F dwarf`, podemos invocar el depurador GNU:
```bash
gdb ./Lab08_Palindromo
(gdb) break _start
(gdb) run
(gdb) layout asm
(gdb) layout regs
(gdb) stepi
```
- Para inspeccionar los caracteres señalados por los punteros:
  ```gdb
  x/c $rsi    # Muestra el carácter izquierdo
  x/c $rdi    # Muestra el carácter derecho
  ```

### 2. ¿Por qué el código de salida es 0 incluso en "NO ES UN PALINDROMO"?
El código de salida del sistema operativo (`exit status` retornado a `$?`) refleja si el proceso se ejecutó de manera exitosa sin errores de runtime. Determinar que una frase no es un palíndromo es una respuesta válida del algoritmo, no un fallo de ejecución. Por el contrario, si la entrada viola las restricciones (&gt; 40 caracteres), el programa sale con código `1` para indicar un error de validación.

---

## 8. Conclusiones

1. **Eficiencia en Bajo Nivel:** El acceso directo a registros de 64 bits (`RSI`, `RDI`, `RAX`) y llamadas al sistema nativas (`sys_read`, `sys_write`) otorga una velocidad de procesamiento insuperable y un uso de memoria extremadamente reducido (menos de 1 KB en BSS).
2. **Procesamiento Preciso de Espacios:** Omitir espacios en blanco y tabulaciones garantiza que las frases del lenguaje natural se analicen conforme a su definición fonética y lógica.
3. **Resistencia ante Entradas Inválidas:** La inclusión de controles de longitud ($\le 40$ caracteres) y avisos ante cadenas vacías o compuestas exclusivamente de espacios dota al software de robustez frente a errores del usuario.
4. **Entrega Completa:** Se disponen de todos los entregables solicitados: código fuente, ejecutables, pruebas automatizadas e informe formal en PDF.
