#pragma once

#include <bitset>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <istream>
#include <ostream>
#include <utility>
#include <vector>

#define let auto&&
#define def auto
#define all(vector) vector.begin(), vector.end()

using ll = long long;
using ull = unsigned long long;

#define range(var, b, e) for (ll var = b; var < e; var++)
// #define with(...) template<typename... __VA_ARGS__>
// #define type typename
#define given auto
#define with(...) template <__VA_ARGS__>
#define arithmeticOperators(op) op(+) op(-) op(*) op(/)
#define mkpair std::pair
#define both(a) a, a

with(typename... Args) def input(Args&&... args)->void {
  ((std::cin >> args), ...);
}

with(typename... Args) def print(Args&&... args)->void {
  ((std::cout << args << ' '), ...);
  std::cout << '\n';
}
using bin = std::bitset<32>;
