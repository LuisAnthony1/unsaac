// Compilación: gcc -m32 -c Lab06_Propuesto2_Sub.c
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
