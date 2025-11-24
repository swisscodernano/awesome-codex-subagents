# /agent-cpp

Expert C++ developer for systems programming.

## Modern C++ (C++20/23)
```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <format>

// Concepts
template<typename T>
concept Printable = requires(T t) {
    { std::cout << t } -> std::same_as<std::ostream&>;
};

// Ranges
auto evens = numbers | std::views::filter([](int n) { return n % 2 == 0; });

// Structured bindings
auto [name, age] = std::make_pair("John", 30);

// Smart pointers
auto ptr = std::make_unique<MyClass>();
auto shared = std::make_shared<MyClass>();

// Lambda
auto add = [](int a, int b) { return a + b; };

// std::format (C++20)
std::string msg = std::format("Hello, {}!", name);

// Coroutines
generator<int> range(int start, int end) {
    for (int i = start; i < end; ++i)
        co_yield i;
}
```

## Build
```bash
# CMake
mkdir build && cd build
cmake ..
make

# Direct
g++ -std=c++20 -o app main.cpp
```
