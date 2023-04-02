#include <iostream>
#include <cstdlib>

int main() {
    int* s0 = nullptr;
    s0 = (int*)std::malloc(sizeof(int));
    *s0 = 0;
    std::cout << "s0 get value: " << *s0 << std::endl;
    std::free(s0);
    return 0;
}
