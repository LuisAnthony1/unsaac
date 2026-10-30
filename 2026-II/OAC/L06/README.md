# Laboratorio 06: Interoperabilidad entre C y Ensamblador NASM (x86 - 32 bits)

**Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)**  
**Departamento Académico de Ingeniería Informática**  
**Organización y Arquitectura del Computador (OAC)** — Semestre 2026-II  
**Docente:** Mgt. Manuel Aurelio Peñaloza Figueroa  
**Estudiante:** Luis Anthony Mamani Mescco (Código: 194522)

---

## 1. Introducción y Objetivos

La interoperabilidad entre el lenguaje de alto nivel **C** y el lenguaje ensamblador **NASM** permite combinar la facilidad de manejo de entrada/salida y estructuras complejas de C con la máxima eficiencia y control a nivel de registros e instrucciones de la arquitectura de la CPU.

### Objetivos:
1. Implementar funciones en NASM invocadas desde un programa principal en C.
2. Invocar funciones escritas en C (y funciones de la biblioteca estándar como `printf` y `scanf`) desde programas principales en NASM.
3. Comprender y aplicar la **convención de llamadas `cdecl`** (C declaration) en arquitectura de 32 bits.
4. Gestionar adecuadamente la pila (*stack*), alineación, pasaje de parámetros en orden inverso y retorno de valores en `EAX`.
5. Respetar la preservación de registros de acuerdo a la convención ABI.

---

## 2. Fundamentos de la Arquitectura x86 (32 bits) y Convención `cdecl`

En modo de 32 bits en Linux, la convención estándar es **`cdecl`**:

| Característica | Detalle en 32-bit (`cdecl`) |
| :--- | :--- |
| **Paso de Parámetros** | Se empujan a la pila (**stack**) en orden inverso (de derecha a izquierda). |
| **Limpieza de la Pila** | Responsabilidad del **llamador** (*Caller*), por ejemplo con `add esp, N`. |
| **Retorno de Valores** | Enteros y direcciones de memoria se retornan en el registro `EAX`. |
| **Registros Preservados (*Callee-saved*)** | `EBX`, `ESI`, `EDI`, `EBP`, `ESP`. Si una subrutina los altera, debe guardarlos (`push`) y restaurarlos (`pop`). |
| **Registros Volátiles (*Caller-saved*)** | `EAX`, `ECX`, `EDX`. Pueden modificarse libremente en subrutinas. |
| **Estructura del Stack Frame** | `push ebp` seguido de `mov ebp, esp`. Los argumentos se acceden en `[ebp + 8]`, `[ebp + 12]`, etc. |

---

## 3. Preinstalación de Dependencias para 32 Bits en Linux

En sistemas Linux modernos de 64 bits (como Ubuntu 22.04 / 24.04 / 26.04), GCC viene por defecto configurado únicamente para generar binarios de 64 bits. Para compilar con la bandera `-m32` y enlazar librerías de 32 bits (`elf32`), se requiere instalar el soporte **multilib**.

### 3.1. Detección del Error Típico
Si no se tienen instaladas las librerías de 32 bits, GCC arrojará errores como:
```text
fatal error: bits/libc-header-start.h: No such file or directory
#include <bits/libc-header-start.h>
         ^~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
```
O errores del enlazador:
```text
/usr/bin/ld: cannot find -lgcc_s: No such file or directory
/usr/bin/ld: skipping incompatible /lib/... when searching for -lc
```

### 3.2. Verificación del Paquete
Para verificar si `gcc-multilib` está presente en el sistema:
```bash
apt-cache policy gcc-multilib
```
Si muestra `Installed: (none)`, no está instalado aún.

### 3.3. Instalación Paso a Paso

#### En distribuciones Ubuntu / Debian:
Ejecutar en la terminal:
```bash
sudo apt update
sudo apt install -y gcc-multilib g++-multilib libc6-dev-i386 nasm
```

#### En otras distribuciones (referencial):
- **Arch Linux / Manjaro:**
  Habilitar el repositorio `[multilib]` en `/etc/pacman.conf` y ejecutar:
  ```bash
  sudo pacman -Syu multilib-devel nasm
  ```
- **Fedora / RHEL:**
  ```bash
  sudo dnf install -y glibc-devel.i686 libgcc.i686 nasm
  ```

### 3.4. Comprobación de Versiones Instaladas
```bash
gcc --version
nasm -v
```

---

## 4. Estructura de Archivos del Laboratorio

```
L06/
├── README.md                      # Esta guía detallada
├── L06-Interoperabilidad entre C y NASM_desbloqueado.pdf  # Guía del laboratorio
├── Lab 6 d OAC.pdf               # Informe oficial presentado
│
├── Lab06_Ejemplo1_Main.c          # Ejemplo 1: C llama función suma en NASM
├── Lab06_Ejemplo1_Sub.asm         # Subrutina en NASM (suma_nasm)
│
├── Lab06_Ejemplo2_Main.asm        # Ejemplo 2: NASM principal con printf/scanf llama suma en C
├── Lab06_Ejemplo2_Sub.c           # Subrutina en C (sumar)
│
├── Lab06_Propuesto1_Main.c        # Propuesto 1: C llama función multiplicación en NASM
├── Lab06_Propuesto1_Sub.asm       # Subrutina en NASM (multiplicar)
│
├── Lab06_Propuesto2_Main.asm      # Propuesto 2: NASM principal llama fibonacci recursivo en C
├── Lab06_Propuesto2_Sub.c         # Subrutina en C (fibonacci)
│
├── Lab06_Propuesto3_Main.c        # Propuesto 3: C llama potencia en NASM
└── Lab06_Propuesto3_Sub.asm       # Subrutina en NASM (potencia con bucle iterativo)
```

---

## 5. Guía Paso a Paso de Compilación y Ejecución

> **Nota Importante:** Para compilar y ejecutar, abra una terminal y ubíquese en esta carpeta:
> ```bash
> cd "/run/media/thony/Nuevo vol/Git/unsaac/2026-II/OAC/L06"
> ```

---

### 5.1. Ejemplo 1: C llama a función NASM (Suma)
- **Lógica:** El programa principal en C solicita dos números mediante `scanf` y llama a la subrutina `suma_nasm(a, b)` implementada en ensamblador. El ensamblador accede a los argumentos mediante `[ebp+8]` y `[ebp+12]`, guarda la suma en `eax` y retorna a C.

#### Paso a Paso:
```bash
# 1. Ensamblar la subrutina en formato ELF 32 bits:
nasm -f elf32 Lab06_Ejemplo1_Sub.asm -o Lab06_Ejemplo1_Sub.o

# 2. Compilar el programa principal en C y enlazar con el objeto NASM:
gcc -m32 Lab06_Ejemplo1_Main.c Lab06_Ejemplo1_Sub.o -o Lab06_Ejemplo1_Main

# 3. Ejecutar:
./Lab06_Ejemplo1_Main
```

#### Ejemplo de Entrada / Salida:
```text
Ingrese el primer número: 12
Ingrese el segundo número: 8
La suma de 12 y 8 es: 20
```

---

### 5.2. Ejemplo 2: NASM llama a función en C y usa `printf` / `scanf`
- **Lógica:** El programa principal está en NASM (`main`). Declara variables en `.bss` y cadenas de formato en `.data`. Llama a `printf` y `scanf` de la biblioteca estándar de C pasando punteros por el stack (`push num1`, etc.), luego invoca la función `int sumar(int a, int b)` escrita en C, imprime el resultado y finaliza con la llamada al sistema `sys_exit` (`int 0x80`).

#### Paso a Paso:
```bash
# 1. Compilar la función en C como código objeto de 32 bits:
gcc -m32 -c Lab06_Ejemplo2_Sub.c -o Lab06_Ejemplo2_Sub.o

# 2. Ensamblar el programa principal NASM en 32 bits:
nasm -f elf32 Lab06_Ejemplo2_Main.asm -o Lab06_Ejemplo2_Main.o

# 3. Enlazar ambos con GCC (usando -no-pie para compatibilidad con código de 32 bits):
gcc -m32 Lab06_Ejemplo2_Main.o Lab06_Ejemplo2_Sub.o -o Lab06_Ejemplo2_Main -no-pie

# 4. Ejecutar:
./Lab06_Ejemplo2_Main
```

#### Ejemplo de Entrada / Salida:
```text
Ingrese el primer numero: 15
Ingrese el segundo numero: 25
La suma es: 40
```

---

### 5.3. Propuesto 1: Multiplicación de dos enteros (C llama a NASM)
- **Lógica:** El programa en C pide dos factores y llama a `extern int multiplicar(int a, int b)`. En ensamblador se realiza `imul eax, [ebp+12]`, retornando el producto en `EAX`.

#### Paso a Paso:
```bash
# 1. Ensamblar subrutina NASM:
nasm -f elf32 Lab06_Propuesto1_Sub.asm -o Lab06_Propuesto1_Sub.o

# 2. Compilar y enlazar con el main en C:
gcc -m32 Lab06_Propuesto1_Main.c Lab06_Propuesto1_Sub.o -o Lab06_Propuesto1_Main

# 3. Ejecutar:
./Lab06_Propuesto1_Main
```

#### Ejemplo de Entrada / Salida:
```text
Ingrese el primer número: 7
Ingrese el segundo número: 6
El producto de [7] y [6] = [42]
```

---

### 5.4. Propuesto 2: Término Fibonacci (NASM llama a función recursiva en C)
- **Lógica:** Ensamblador pide un entero $n$ con `scanf`, apila el parámetro y llama a `fibonacci(n)` implementada de forma recursiva en C. Luego muestra el resultado formateado con `printf`.

#### Paso a Paso:
```bash
# 1. Compilar función C recursiva a objeto de 32 bits:
gcc -m32 -c Lab06_Propuesto2_Sub.c -o Lab06_Propuesto2_Sub.o

# 2. Ensamblar programa NASM:
nasm -f elf32 Lab06_Propuesto2_Main.asm -o Lab06_Propuesto2_Main.o

# 3. Enlazar con GCC en 32 bits (-no-pie):
gcc -m32 Lab06_Propuesto2_Main.o Lab06_Propuesto2_Sub.o -o Lab06_Propuesto2_Main -no-pie

# 4. Ejecutar:
./Lab06_Propuesto2_Main
```

#### Ejemplo de Entrada / Salida:
```text
Ingrese n: 10
El término Fibonacci de (10) = 55
```

---

### 5.5. Propuesto 3: Potencia $base^{exponente}$ (C llama a NASM con preservación de registros)
- **Lógica:** El programa en C solicita base y exponente. La subrutina en NASM calcula la potencia mediante un ciclo iterativo `imul eax, ebx; dec ecx; jmp .ciclo`.
  
  > **Aspecto Crítico de Arquitectura:** Dado que la subrutina utiliza `EBX` para almacenar la base, debe **preservar** dicho registro según la convención `cdecl` (`push ebx` al inicio y `pop ebx` antes de `ret`). Si no se preserva `EBX`, el entorno de ejecución de C puede corromperse.

#### Paso a Paso:
```bash
# 1. Ensamblar subrutina NASM:
nasm -f elf32 Lab06_Propuesto3_Sub.asm -o Lab06_Propuesto3_Sub.o

# 2. Compilar y enlazar con C:
gcc -m32 Lab06_Propuesto3_Main.c Lab06_Propuesto3_Sub.o -o Lab06_Propuesto3_Main

# 3. Ejecutar:
./Lab06_Propuesto3_Main
```

#### Ejemplo de Entrada / Salida:
```text
Ingrese la base: 2
Ingrese el exponente: 8
El resultado de 2 elevado a 8 = 256
```

---

## 6. Script de Compilación Automatizada

Para compilar todos los ejercicios de una sola vez, puede ejecutar el siguiente bloque de comandos:

```bash
# Compilar Ejemplo 1
nasm -f elf32 Lab06_Ejemplo1_Sub.asm -o Lab06_Ejemplo1_Sub.o
gcc -m32 Lab06_Ejemplo1_Main.c Lab06_Ejemplo1_Sub.o -o Lab06_Ejemplo1_Main

# Compilar Ejemplo 2
gcc -m32 -c Lab06_Ejemplo2_Sub.c -o Lab06_Ejemplo2_Sub.o
nasm -f elf32 Lab06_Ejemplo2_Main.asm -o Lab06_Ejemplo2_Main.o
gcc -m32 Lab06_Ejemplo2_Main.o Lab06_Ejemplo2_Sub.o -o Lab06_Ejemplo2_Main -no-pie

# Compilar Propuesto 1
nasm -f elf32 Lab06_Propuesto1_Sub.asm -o Lab06_Propuesto1_Sub.o
gcc -m32 Lab06_Propuesto1_Main.c Lab06_Propuesto1_Sub.o -o Lab06_Propuesto1_Main

# Compilar Propuesto 2
gcc -m32 -c Lab06_Propuesto2_Sub.c -o Lab06_Propuesto2_Sub.o
nasm -f elf32 Lab06_Propuesto2_Main.asm -o Lab06_Propuesto2_Main.o
gcc -m32 Lab06_Propuesto2_Main.o Lab06_Propuesto2_Sub.o -o Lab06_Propuesto2_Main -no-pie

# Compilar Propuesto 3
nasm -f elf32 Lab06_Propuesto3_Sub.asm -o Lab06_Propuesto3_Sub.o
gcc -m32 Lab06_Propuesto3_Main.c Lab06_Propuesto3_Sub.o -o Lab06_Propuesto3_Main

echo "Todos los binarios han sido compilados con éxito."
```

Para limpiar archivos objeto y ejecutables temporales:
```bash
rm -f *.o Lab06_Ejemplo1_Main Lab06_Ejemplo2_Main Lab06_Propuesto1_Main Lab06_Propuesto2_Main Lab06_Propuesto3_Main
```

---

## 7. Preguntas Frecuentes y Consejos de Depuración

1. **¿Por qué se usa `-no-pie` en GCC?**  
   Las distribuciones modernas de Linux compilan binarios como *Position Independent Executables* (PIE) por defecto. Cuando el punto de entrada es ensamblador en 32 bits sin soporte para tablas de reubicación PIC, `-no-pie` evita errores de reubicación estática.

2. **¿Por qué la directiva `section .note.GNU-stack noalloc noexec nowrite progbits`?**  
   Esta sección le indica al enlazador de Linux que la pila no requiere permisos de ejecución, eliminando advertencias como:  
   `ld: warning: ... has a LOAD segment with executable stack`.

3. **¿Cómo depurar con GDB?**  
   Para depurar ensamblado y código C paso a paso:
   ```bash
   nasm -g -F dwarf -f elf32 Lab06_Ejemplo1_Sub.asm -o Lab06_Ejemplo1_Sub.o
   gcc -g -m32 Lab06_Ejemplo1_Main.c Lab06_Ejemplo1_Sub.o -o Lab06_Ejemplo1_Main
   gdb ./Lab06_Ejemplo1_Main
   ```
   Comandos útiles dentro de GDB: `layout asm`, `layout regs`, `stepi`, `info registers`.
