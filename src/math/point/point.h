#pragma once

#include "../../utils/utils.h"
#include "../float/float.h"
namespace math {

// 2d point, (x, y)
struct Point {
  ft x{0}, y{0};
  Point() = default;
  Point(ft x, ft y) : x(x), y(y){};
};

// {0.0, 0.0}
const Point ORIGIN{0, 0};

// some macros for arithmetic overload
#define pointFtOpDefinition(op) Point operator op(Point p, ft c);
#define ftPointOpDefinition(op) Point operator op(ft c, Point p);

// point and float arithmetic overload
// (+, -, *, /)
// 1. Point & float
arithmeticOperators(pointFtOpDefinition);
// 2. Float & Point
arithmeticOperators(ftPointOpDefinition);

// i like point, the more the betteeer
using Points = std::vector<Point>;

// syntatic sugar for point i/o
std::ostream& operator<<(std::ostream& os, const Point& p);
std::ostream& operator<<(std::ostream& os, const Points& p);
std::istream& operator>>(std::istream& is, Point& p);

}  // namespace math
