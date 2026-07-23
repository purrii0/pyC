int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int gcd(int a, int b) {
    while (b != 0) {
        int t;
        t = b;
        b = a - (a / b) * b;
        a = t;
    }
    return a;
}

char classify(int n) {
    if (n < 0) {
        return 'n';
    } else {
        if (n == 0) {
            return 'z';
        } else {
            return 'p';
        }
    }
}

int main() {
    int a;
    int b;
    printf("Enter two integers: ");
    scanf("%d", &a);
    scanf("%d", &b);

    printf("gcd(%d, %d) = %d\n", a, b, gcd(a, b));

    int n;
    n = 5;
    printf("factorial(%d) = %d\n", n, factorial(n));

    char c;
    c = classify(a - b);
    printf("classification: %c\n", c);

    return 0;
}