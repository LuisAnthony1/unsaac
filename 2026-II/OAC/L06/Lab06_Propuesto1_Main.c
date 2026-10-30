// Compilación: gcc -m32 Lab06_Propuesto1_Main.c Lab06_Propuesto1_Sub.o -o Lab06_Propuesto1_Main
// Ejecución: ./Lab06_Propuesto1_Main
#include <stdio.h>

extern int multiplicar(int a, int b);

int main() {
    int a, b;
    printf("Ingrese el primer número: ");
    scanf("%d", &a);
    printf("Ingrese el segundo número: ");
    scanf("%d", &b);
    
    int resultado = multiplicar(a, b);
    printf("El producto de [%d] y [%d] = [%d]\n", a, b, resultado);
    return 0;
}
