int fib(int n) {
  if (n < 2) {
    return n;
  }
  return fib(n - 1) + fib(n - 2);
}

int main() {
  int x = 0;
  while (x != 10) {
    x = x + 1;
  }
  return fib(10);
}