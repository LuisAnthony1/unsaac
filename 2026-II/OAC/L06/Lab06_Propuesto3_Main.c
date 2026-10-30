// Compilación: gcc -m32 Lab06_Propuesto3_Main.c Lab06_Propuesto3_Sub.o -o Lab06_Propuesto3_Main
// Ejecución: ./Lab06_Propuesto3_Main
#include <stdio.h>

extern int potencia(int base, int exponente);

int main() {
    int base, exp;
    printf("Ingrese la base: ");
    scanf("%d", &base);
    printf("Ingrese el exponente: ");
    scanf("%d", &exp);
    
    int resultado = potencia(base, exp);
    printf("El resultado de %d elevado a %d = %d\n", base, exp, resultado);
    return 0;
}
