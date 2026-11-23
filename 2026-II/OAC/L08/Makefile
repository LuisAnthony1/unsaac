# ==============================================================================
# UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
# DEPARTAMENTO ACADÉMICO DE INGENIERÍA INFORMÁTICA
# ORGANIZACIÓN Y ARQUITECTURA DEL COMPUTADOR - LABORATORIO 08
#
# Makefile de Automatización para NASM x86-64 y x86 (32 bits)
# Autor: Luis Anthony Mamani Mescco (Código: 194522)
# ==============================================================================

NASM      := nasm
LD        := ld
RM        := rm -f

# Banderas x86-64
ASM_FLAGS_64 := -f elf64 -g -F dwarf
LD_FLAGS_64  :=

# Banderas x86-32
ASM_FLAGS_32 := -f elf32 -g -F dwarf
LD_FLAGS_32  := -m elf_i386

TARGETS_64 := Lab08_Palindromo Lab08_Propuesto1
TARGETS_32 := Lab08_Palindromo_32

.PHONY: all 64 32 clean run test

all: 64

64: $(TARGETS_64)

32: $(TARGETS_32)

# Reglas para 64 bits
Lab08_Palindromo: Lab08_Palindromo.o
	$(LD) $(LD_FLAGS_64) -o $@ $<
	chmod +x $@

Lab08_Palindromo.o: Lab08_Palindromo.asm
	$(NASM) $(ASM_FLAGS_64) $< -o $@

Lab08_Propuesto1: Lab08_Propuesto1.o
	$(LD) $(LD_FLAGS_64) -o $@ $<
	chmod +x $@

Lab08_Propuesto1.o: Lab08_Propuesto1.asm
	$(NASM) $(ASM_FLAGS_64) $< -o $@

# Reglas para 32 bits
Lab08_Palindromo_32: Lab08_Palindromo_32.o
	$(LD) $(LD_FLAGS_32) -o $@ $<
	chmod +x $@

Lab08_Palindromo_32.o: Lab08_Palindromo_32.asm
	$(NASM) $(ASM_FLAGS_32) $< -o $@

clean:
	$(RM) *.o $(TARGETS_64) $(TARGETS_32)

run: Lab08_Palindromo
	./Lab08_Palindromo
