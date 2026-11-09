# Laboratorio 07: Operaciones Aritméticas en x64 (Multiplicación, División Entera, Módulo y Precisión Decimal)

**Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)**  
**Departamento Académico de Ingeniería Informática**  
**Organización y Arquitectura del Computador (OAC)** — Semestre 2026-II  
**Docente:** Mgt. Manuel Aurelio Peñaloza Figueroa  
**Estudiante:** Luis Anthony Mamani Mescco (Código: 194522)

---

## 1. Introducción y Objetivos

En el presente laboratorio se abordan las operaciones aritméticas fundamentales en bajo nivel para la arquitectura **x86-64 (AMD64)** bajo Linux. A diferencia de laboratorios anteriores donde se utilizaba la biblioteca estándar de C (`printf`, `scanf`) y modo de 32 bits, este laboratorio implementa programas **independientes en ensamblador NASM puro de 64 bits**, comunicándose directamente con el kernel de Linux a través de llamadas al sistema (*syscalls*) sin sobrecarga de bibliotecas externas (*libc*).

### Objetivos:
1. **Dominar la Entrada/Salida en x86-64 puro:** Gestionar buffers en memoria y realizar lecturas (`sys_read`) y escrituras (`sys_write`) directas mediante la instrucción `syscall`.
2. **Aplicar Instrucciones Aritméticas Avanzadas:** Emplear `IMUL`, `IDIV`, `DIV`, `MUL` y la instrucción de extensión de signo `CQO` en registros de 64 bits (`RAX`, `RBX`, `RDX`, `RSI`, `RDI`).
3. **Manejar la Representación con Signo:** Implementar algoritmos de conversión de cadenas ASCII a enteros con signo en **Complemento a 2** y viceversa (`str_to_int`, `int_to_str`).
4. **Implementar División Decimal Fija:** Desarrollar el cálculo de división decimal escalando previamente el dividendo ($10^4$) para obtener una precisión fija de 4 decimales con alineación de ceros a la izquierda.
5. **Implementar División Decimal de Precisión Variable Arbitraria:** Diseñar un algoritmo de **división larga dígito por dígito** capaz de generar $\ge 20$ decimales (parametrizable de 0 a 100 decimales), superando la limitación de registros de 64 bits mediante operaciones intermedias de 128 bits.
6. **Implementar Validaciones de Robustez y Control de Errores:** Prevenir excepciones críticas del procesador como la división entre cero (`SIGFPE`), el desbordamiento de división en el caso límite $-2^{63} \div -1$, y detectar overflow en multiplicaciones con la bandera `OF`.

---

## 2. Fundamentos de la Arquitectura x86-64 y Aritmética de Enteros

### 2.1. Representación en Complemento a 2
Los enteros con signo de 64 bits se almacenan en formato de Complemento a 2:
- El bit más significativo (**MSB**, bit 63) determina el signo: `0` para positivo o cero, `1` para negativo.
- **Rango representable:** $[-2^{63}, 2^{63} - 1]$, es decir:
  $$\text{Rango} = [-9\,223\,372\,036\,854\,775\,808,\; 9\,223\,372\,036\,854\,775\,807]$$
- Negar un número en Complemento a 2 equivale a invertir todos los bits y sumar 1 (`neg reg`).

### 2.2. Multiplicación con Signo (`IMUL`)
En x86-64, la instrucción `IMUL` realiza la multiplicación respetando la ley de los signos:
$$(+) \times (+) = (+), \quad (-) \times (-) = (+), \quad (+) \times (-) = (-), \quad (-) \times (+) = (-)$$

Formas sintácticas principales:
1. **Forma de 2 operandos:** `imul reg64, r/m64` $\rightarrow$ `reg64 = reg64 * r/m64`. Si el producto excede 64 bits, se activan las banderas de acarreo y desbordamiento (`CF = 1`, `OF = 1`), permitiendo detectar overflow con la instrucción `JO` (*Jump if Overflow*).
2. **Forma de 1 operando:** `imul r/m64` $\rightarrow$ Multiplica `RAX * r/m64` y almacena el resultado completo de 128 bits en el par de registros `RDX:RAX`.

### 2.3. División Entera y Módulo con Signo (`IDIV`)
La instrucción `IDIV r/m64` divide el valor de **128 bits** contenido en `RDX:RAX` entre el operando divisor de 64 bits.

#### Reglas críticas de operación:
1. **Extensión de signo obligatoria (`CQO`):** Antes de ejecutar `IDIV`, se debe extender el bit de signo de `RAX` a través de los 64 bits de `RDX` usando la instrucción `CQO` (*Convert Quadword to Octword*). Si `RDX` no se inicializa con `CQO`, contendrá valores espurios y provocará un cálculo erróneo o una excepción inmediata.
2. **Signo del Cociente (`RAX`):** Positivo si dividendo y divisor tienen el mismo signo; negativo si tienen signos opuestos.
3. **Signo del Residuo / Módulo (`RDX`):** **El residuo siempre toma el signo del dividendo**, independientemente del signo del divisor:
   
   | Dividendo | Divisor | Cociente (`RAX`) | Residuo (`RDX`) | Verificación ($a = q \cdot b + r$) |
   | :---: | :---: | :---: | :---: | :---: |
   | `15` | `4` | `3` | `3` | $15 = 3 \cdot 4 + 3$ |
   | `-15` | `4` | `-3` | `-3` | $-15 = (-3) \cdot 4 + (-3)$ |
   | `15` | `-4` | `-3` | `3` | $15 = (-3) \cdot (-4) + 3$ |
   | `-15` | `-4` | `3` | `-3` | $-15 = 3 \cdot (-4) + (-3)$ |

4. **Casos Críticos de Excepción de Hardware:**
   - **División por cero:** La CPU emite una interrupción tipo 0 (`#DE` - Divide Error), traducida por el kernel de Linux como señal `SIGFPE` (*Floating point exception*), abortando el programa si no se valida previamente.
   - **Desbordamiento de división:** El valor mínimo negativo $-2^{63}$ dividido entre $-1$ requeriría $+2^{63}$, el cual no cabe en un entero con signo de 64 bits (máximo $+2^{63} - 1$). Provoca también una excepción `#DE`.

### 2.4. Estrategias de División Decimal en Ensamblador

#### A) Método de Escalado Previo (Propuesto 1 - 4 decimales)
Consiste en multiplicar el dividendo por $10^4 = 10\,000$ antes de realizar la división:
$$\text{Cociente Escalado} = \frac{\text{Dividendo} \times 10\,000}{\text{Divisor}}$$
- **Parte entera:** $\lfloor |\text{Cociente Escalado}| / 10\,000 \rfloor$
- **Parte fraccionaria:** $|\text{Cociente Escalado}| \pmod{10\,000}$
- La parte fraccionaria se formatea con ceros a la izquierda garantizando 4 dígitos (por ejemplo, $50 \rightarrow \text{"0050"}$).

#### B) Método de División Larga (Propuesto 2 - Precisión variable $\ge 20$ decimales)
Para una precisión de 20 o más decimales, un factor de escalado como $10^{20}$ no puede usarse directamente porque excede el rango máximo de un registro de 64 bits ($10^{20} > 2^{64} - 1 \approx 1.84 \times 10^{19}$).

Se implementa el algoritmo de **división larga dígito a dígito**:
1. Trabajar con los valores absolutos $|a|$ y $|b|$, registrando el signo resultante: $\text{signo} = \text{MSB}(a \oplus b)$.
2. Calcular la parte entera inicial y su residuo $r_0$:
   $$\text{parte\_entera} = |a| / |b|, \quad r_0 = |a| \pmod{|b|}$$
3. Por cada posición decimal requerida ($i = 1, \dots, N$):
   - Multiplicar el residuo actual por 10: $(r_{i-1} \times 10)$ usando `MUL` de 128 bits (`RDX:RAX = RAX * 10`), garantizando que jamás ocurra desbordamiento.
   - Extraer el nuevo dígito decimal y el nuevo residuo:
     $$d_i = (r_{i-1} \times 10) / |b|, \quad r_i = (r_{i-1} \times 10) \pmod{|b|}$$
   - Convertir $d_i$ a carácter ASCII (`add dl, '0'`) y almacenar secuencialmente en el buffer.
4. El resultado final se trunca exactamente a $N$ cifras decimales.

---

### 2.5. Llamadas al Sistema (*Syscalls*) en Linux x86-64

En Linux de 64 bits se utiliza la instrucción nativa `syscall` (reemplazo de `int 0x80` de 32 bits), siguiendo la convención **System V AMD64 ABI**:

| Parámetro | Registro en x86-64 (`syscall`) | Registro en x86-32 (`int 0x80`) |
| :--- | :---: | :---: |
| **Identificador de Syscall** | `RAX` | `EAX` |
| **Argumento 1 (File Descriptor)** | `RDI` | `EBX` |
| **Argumento 2 (Puntero a Buffer)** | `RSI` | `ECX` |
| **Argumento 3 (Longitud en bytes)** | `RDX` | `EDX` |
| **Argumento 4** | `R10` | `ESI` |
| **Argumento 5** | `R8` | `EDI` |
| **Valor de Retorno** | `RAX` | `EAX` |

#### Syscalls utilizadas en este laboratorio:
- **`sys_read` (RAX = 0):** Lee bytes desde `stdin` (`RDI = 0`).
- **`sys_write` (RAX = 1):** Escribe bytes a `stdout` (`RDI = 1`).
- **`sys_exit` (RAX = 60):** Finaliza el proceso devolviendo el código en `RDI` (0 para éxito, 1 para error).

---

## 3. Requisitos y Herramientas de Desarrollo

Para ensamblar y enlazar los programas en cualquier sistema Linux moderno de 64 bits se requieren:
- **NASM:** Netwide Assembler versión 2.15 o superior (compatible y probado en NASM 3.01).
- **GNU ld:** Enlazador del paquete `binutils`.

### Comprobación de instalación:
```bash
nasm -v
ld -v
```

Si faltase alguna herramienta en Debian/Ubuntu:
```bash
sudo apt update
sudo apt install -y nasm binutils
```

> [!NOTE]
> Todos los archivos fuente `.asm` siguen el formato de comentarios estándar de la guía docente (`Programa`, `Compilación`, `Linkeado`, `Ejecución`) sin directivas adicionales, listos para ser ensamblados y enlazados directamente desde la terminal.

---

## 4. Estructura de Archivos del Laboratorio

Siguiendo el estándar y convención de nombres de los laboratorios del curso (como en el Laboratorio 06):

```
L07/
├── README.md                                  # Guía completa de arquitectura, compilación y pruebas
├── L07-Operaciones Aritméticas en x64 v.13.docx - L07-Operaciones Aritméticas en x64.pdf  # Guía oficial PDF
│
├── Lab07_Ejemplo1.asm                         # Práctica 1 (5.1-1): Multiplicación, División Entera y Módulo
├── Lab07_Practica1.asm                        # Práctica 1 (5.1-1, nombre alternativo)
├── Lab07_Propuesto1.asm                       # Propuesto 1 (6.1): División decimal fija (4 decimales)
└── Lab07_Propuesto2.asm                       # Propuesto 2 (6.2): Precisión variable (0 a 100 decimales)
```

### Generación de Ejecutables
En los sistemas operativos tipo Unix/Linux, el usuario ensambla con `nasm -f elf64` y enlaza con `ld` para generar los binarios **ELF** sin extensión (listos para ejecución con `./nombre_programa`).

La guía del docente solicita expresamente:
> *"Adjuntar los respectivos códigos .asm, y los ejecutables (los nombres de los ejecutables deberán claramente referenciar a que ejercicio propuesto corresponden)."*

---

## 5. Guía Paso a Paso de Compilación y Ejecución

> **Ubicación:** Abra una terminal y sitúese en el directorio del laboratorio:
> ```bash
> cd "/run/media/thony/Nuevo vol/Git/unsaac/2026-II/OAC/L07"
> ```

---

### 5.1. Práctica 1 (`Lab07_Practica1.asm`) — Trabajo de Laboratorio (Sección 5.1-1)
- **Lógica:** Solicita dos números enteros con signo, ejecuta `imul rax, rbx` para la multiplicación, prepara `cqo` y ejecuta `idiv rbx` para obtener el cociente en `RAX` y el residuo en `RDX`. Finalmente convierte cada valor numérico a texto ASCII y lo muestra por pantalla.

#### Compilación y Enlace:
```bash
# 1. Ensamblar a código objeto ELF 64 bits:
nasm -f elf64 Lab07_Practica1.asm -o Lab07_Practica1.o

# 2. Enlazar directamente con GNU ld:
ld Lab07_Practica1.o -o Lab07_Practica1

# 3. Asignar permisos de ejecución (si fuese necesario):
chmod +x Lab07_Practica1

# 4. Ejecutar:
./Lab07_Practica1
```

#### Casos de Prueba Verificados:

**Caso A: Ambos números positivos (15 y 4)**
```text
$ ./Lab07_Practica1
Ingrese el 1er numero: 15
Ingrese el 2do numero: 4
Multiplicacion: 60
Division entera: 3
Modulo: 3
```

**Caso B: Dividendo negativo (-15 y 4)**
```text
$ ./Lab07_Practica1
Ingrese el 1er numero: -15
Ingrese el 2do numero: 4
Multiplicacion: -60
Division entera: -3
Modulo: -3
```

**Caso C: Divisor negativo (15 y -4)**
```text
$ ./Lab07_Practica1
Ingrese el 1er numero: 15
Ingrese el 2do numero: -4
Multiplicacion: -60
Division entera: -3
Modulo: 3
```

**Caso D: Ambos números negativos (-15 y -4)**
```text
$ ./Lab07_Practica1
Ingrese el 1er numero: -15
Ingrese el 2do numero: -4
Multiplicacion: 60
Division entera: 3
Modulo: -3
```

> [!NOTE]
> En el caso D: $(-15) \div (-4) = 3$ con módulo $-3$. El residuo en `IDIV` preserva estrictamente el signo del dividendo, cumpliendo con la especificación de arquitectura de la guía teórica.

---

### 5.2. Ejercicio Propuesto 1 (`Lab07_Propuesto1.asm`) — División Decimal Fija (Sección 6.1)
- **Lógica:** Implementa multiplicación, división entera, módulo y **división decimal con 4 decimales** calculada mediante escalado previo ($10^4 = 10\,000$). Incorpora validación de división entre cero, detección de overflow en `IMUL` (`JO`), y detección del desbordamiento crítico de hardware $-2^{63} \div -1$.

#### Compilación y Enlace:
```bash
# 1. Ensamblar:
nasm -f elf64 Lab07_Propuesto1.asm -o Lab07_Propuesto1.o

# 2. Enlazar:
ld Lab07_Propuesto1.o -o Lab07_Propuesto1

# 3. Asignar permisos y ejecutar:
chmod +x Lab07_Propuesto1
./Lab07_Propuesto1
```

#### Casos de Prueba Verificados:

**Caso A: División periódica estándar (10 y 3)**
```text
$ ./Lab07_Propuesto1
Ingrese el 1er numero: 10
Ingrese el 2do numero: 3
Multiplicacion: 30
Division entera: 3
Modulo: 1
Division decimal (4 decimales): 3.3333
```

**Caso B: Operando negativo (-150 y 7)**
```text
$ ./Lab07_Propuesto1
Ingrese el 1er numero: -150
Ingrese el 2do numero: 7
Multiplicacion: -1050
Division entera: -21
Modulo: -3
Division decimal (4 decimales): -21.4285
```

**Caso C: Alineación con ceros a la izquierda (1 y 200)**
```text
$ ./Lab07_Propuesto1
Ingrese el 1er numero: 1
Ingrese el 2do numero: 200
Multiplicacion: 200
Division entera: 0
Modulo: 1
Division decimal (4 decimales): 0.0050
```

**Caso D: Validación de División por Cero (5 y 0)**
```text
$ ./Lab07_Propuesto1
Ingrese el 1er numero: 5
Ingrese el 2do numero: 0
Multiplicacion: 0
Error: division por cero.
```

---

### 5.3. Ejercicio Propuesto 2 (`Lab07_Propuesto2.asm`) — Precisión Variable (Sección 6.2)
- **Lógica:** Solicita el dividendo, el divisor y la **cantidad de cifras decimales** deseadas por el usuario (rango válido de 0 a 100, cumpliendo con creces el requisito de al menos 20 decimales). Utiliza el algoritmo de **división larga dígito a dígito** con escalado del residuo en 128 bits mediante `MUL rcx` (`RDX:RAX`).

#### Compilación y Enlace:
```bash
# 1. Ensamblar:
nasm -f elf64 Lab07_Propuesto2.asm -o Lab07_Propuesto2.o

# 2. Enlazar:
ld Lab07_Propuesto2.o -o Lab07_Propuesto2

# 3. Asignar permisos y ejecutar:
chmod +x Lab07_Propuesto2
./Lab07_Propuesto2
```

#### Casos de Prueba Verificados:

**Caso A: Mínimo requerido de 20 decimales ($1 \div 7$ con 20 cifras)**
```text
$ ./Lab07_Propuesto2
Ingrese el 1er numero: 1
Ingrese el 2do numero: 7
Ingrese el numero de decimales (0 a 100): 20
Multiplicacion: 7
Division entera: 0
Modulo: 1
Division decimal: 0.14285714285714285714
```

**Caso B: Aproximación de $\pi$ ($22 \div 7$ con 10 decimales)**
```text
$ ./Lab07_Propuesto2
Ingrese el 1er numero: 22
Ingrese el 2do numero: 7
Ingrese el numero de decimales (0 a 100): 10
Multiplicacion: 154
Division entera: 3
Modulo: 1
Division decimal: 3.1428571428
```

**Caso C: Negativo periódico ($-10 \div 3$ con 6 decimales)**
```text
$ ./Lab07_Propuesto2
Ingrese el 1er numero: -10
Ingrese el 2do numero: 3
Ingrese el numero de decimales (0 a 100): 6
Multiplicacion: -30
Division entera: -3
Modulo: -1
Division decimal: -3.333333
```

**Caso D: Alta precisión ($1 \div 3$ con 50 decimales)**
```text
$ ./Lab07_Propuesto2
Ingrese el 1er numero: 1
Ingrese el 2do numero: 3
Ingrese el numero de decimales (0 a 100): 50
Multiplicacion: 3
Division entera: 0
Modulo: 1
Division decimal: 0.33333333333333333333333333333333333333333333333333
```

**Caso E: Validación de rango de decimales (101 decimales ingresados)**
```text
$ ./Lab07_Propuesto2
Ingrese el 1er numero: 1
Ingrese el 2do numero: 3
Ingrese el numero de decimales (0 a 100): 101
Error: el numero de decimales debe estar entre 0 y 100.
```

---

## 6. Script de Compilación Automatizada

Para compilar todos los programas del laboratorio de forma simultánea, puede copiar y pegar el siguiente bloque en su terminal:

```bash
# Compilar Práctica 1
nasm -f elf64 Lab07_Practica1.asm -o Lab07_Practica1.o
ld Lab07_Practica1.o -o Lab07_Practica1
chmod +x Lab07_Practica1

# Compilar Propuesto 1
nasm -f elf64 Lab07_Propuesto1.asm -o Lab07_Propuesto1.o
ld Lab07_Propuesto1.o -o Lab07_Propuesto1
chmod +x Lab07_Propuesto1

# Compilar Propuesto 2
nasm -f elf64 Lab07_Propuesto2.asm -o Lab07_Propuesto2.o
ld Lab07_Propuesto2.o -o Lab07_Propuesto2
chmod +x Lab07_Propuesto2

echo "Todos los programas del Laboratorio 07 han sido ensamblados y enlazados exitosamente."
```

### Limpieza de Archivos Objeto Temporales:
```bash
rm -f *.o
```

---

## 7. Preguntas Frecuentes y Consejos de Depuración

### 1. ¿Por qué el punto de entrada es `_start` y no `main`?
En programas que enlazan con la biblioteca estándar de C (`gcc`), el punto de entrada inicial del sistema operativo es `_start` (provisto por `crt1.o`), el cual inicializa el entorno de C y luego invoca a la función de usuario `main`.  
Al enlazar directamente con `ld` sin biblioteca de C, nuestro programa debe definir su propio punto de entrada `_start:` y finalizar llamando explícitamente a `sys_exit` (`rax = 60, syscall`).

### 2. ¿Por qué se debe usar `CQO` antes de `IDIV`?
La instrucción `IDIV rbx` no divide únicamente `RAX`; divide el par formado por `RDX:RAX` (128 bits). Si `RAX` tiene un número con signo negativo (por ejemplo, $-15$), su bit 63 es `1`. La instrucción `cqo` propaga ese bit `1` a todos los bits de `RDX` (`0xFFFFFFFFFFFFFFFF`), representando correctamente el valor $-15$ en 128 bits. Si no se ejecuta `cqo`, `RDX` mantendrá cualquier valor previo, alterando por completo la operación.

### 3. ¿Cómo evitar el signo negativo en ceros fraccionarios (ej. `-0.000`)?
En el ejercicio propuesto 2, si se calcula un valor muy pequeño cuyo resultado truncado es cero pero los signos de dividendo y divisor eran opuestos, el algoritmo verifica el acumulador de magnitud `R11`. Si todos los dígitos generados son cero, suprime el signo negativo para no emitir una salida matemáticamente incómoda como `-0.000`.

### 4. Depuración Paso a Paso con GDB:
Para inspeccionar registros de 64 bits (`RAX`, `RDX`, flags) durante la ejecución:
```bash
# Ensamblar con información de depuración DWARF:
nasm -g -F dwarf -f elf64 Lab07_Practica1.asm -o Lab07_Practica1.o
ld Lab07_Practica1.o -o Lab07_Practica1

# Iniciar GDB:
gdb ./Lab07_Practica1
```
Comandos recomendados en GDB:
- `layout asm` : Muestra el desensamblado en tiempo real.
- `layout regs`: Muestra los registros generales de 64 bits y sus banderas.
- `stepi` / `si`: Ejecuta una sola instrucción máquina.
- `p/x $rax`    : Imprime `RAX` en hexadecimal.
- `p/d $rax`    : Imprime `RAX` en decimal con signo.
- `info registers`: Muestra el estado completo de los registros de la CPU.

