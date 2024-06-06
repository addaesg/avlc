#include "point.h"

namespace math {

#define pointFtOp(op) \
  Point operator op(Point p, ft c) { return {p.x op c, p.y op c}; }

#define ftPointOp(op) \
  Point operator op(ft c, Point p) { return p op c; }

// point and float arithmetic overload
// (+, -, *, /)
// 1. Point & float
arithmeticOperators(pointFtOp);

// 2. Float & Point
arithmeticOperators(ftPointOp);

// Print sintax sugar for point
std::ostream& operator<<(std::ostream& os, const Point& p) {
  os << (float)p.x << ' ' << (float)p.y << '\n';
  return os;
}

// Input sintax sugar for point
std::istream& operator>>(std::istream& is, Point& p) {
  is >> p.x >> p.y;
  return is;
}

// Print sintax sugar for points
std::ostream& operator<<(std::ostream& os, const Points& ps) {
  for (const Point& p : ps) os << p;
  return os;
}
}  // namespace math
