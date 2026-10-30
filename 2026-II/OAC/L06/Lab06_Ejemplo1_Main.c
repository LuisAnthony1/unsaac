// Compilación: gcc -m32 Lab06_Ejemplo1_Main.c Lab06_Ejemplo1_Sub.o -o Lab06_Ejemplo1_Main
// Ejecución: ./Lab06_Ejemplo1_Main
#include <stdio.h>

extern int suma_nasm(int a, int b);

int main() {
    int a, b;
    printf("Ingrese el primer número: ");
    scanf("%d", &a);
    printf("Ingrese el segundo número: ");
    scanf("%d", &b);
    
    int resultado = suma_nasm(a, b);
    printf("La suma de %d y %d es: %d\n", a, b, resultado);
    return 0;
}
