#!/bin/bash
# ==============================================================================
# Script de compilacion automatica para el Laboratorio 08
# Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)
# ==============================================================================

set -e

echo "=== [1/3] Compilando Lab08_Palindromo (x86-64) ==="
nasm -f elf64 Lab08_Palindromo.asm -o Lab08_Palindromo.o
ld Lab08_Palindromo.o -o Lab08_Palindromo
chmod +x Lab08_Palindromo
echo "-> Generado: ./Lab08_Palindromo"

echo "=== [2/3] Compilando Lab08_Propuesto1 (x86-64) ==="
nasm -f elf64 Lab08_Propuesto1.asm -o Lab08_Propuesto1.o
ld Lab08_Propuesto1.o -o Lab08_Propuesto1
chmod +x Lab08_Propuesto1
echo "-> Generado: ./Lab08_Propuesto1"

echo "=== [3/3] Compilando Lab08_Palindromo_32 (x86 32 bits opcional) ==="
if ld -m elf_i386 --help >/dev/null 2>&1; then
    nasm -f elf32 Lab08_Palindromo_32.asm -o Lab08_Palindromo_32.o
    ld -m elf_i386 Lab08_Palindromo_32.o -o Lab08_Palindromo_32
    chmod +x Lab08_Palindromo_32
    echo "-> Generado: ./Lab08_Palindromo_32"
else
    echo "-> Omitido: Soporte de 32-bit (elf_i386) no instalado en el linker."
fi

# Limpieza de temporales .o
rm -f *.o

echo ""
echo "============================================================"
echo "Compilacion finalizada exitosamente."
echo "Para ejecutar el programa principal:"
echo "    ./Lab08_Palindromo"
echo "============================================================"
