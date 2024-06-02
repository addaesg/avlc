#pragma once

#include "../point/point.h"
#include "../trigonometry/trigonometry.h"

namespace math {

class Circle {
 private:
  Point center_{0, 0};
  ft radius_{1.0};

 public:
  Circle() = default;
  Circle(Point center, ft radius) : center_(center), radius_(radius){};
  // Circle center
  def inline center() const->Point { return (*this).center_; };
  // Circle radius
  def inline radius() const->ft { return (*this).radius_; };

  def inline setCenter(Point pos)->void { (*this).center_ = pos; };
  def inline setRadius(ft radius)->void 
  { (*this).radius_ = radius; };

  // get points on the circunference
  def samplePoints(ull sampleCount = 1000) const->Points;
};

std::ostream& operator<<(std::ostream& os, const Circle& c);
std::istream& operator>>(std::istream& is, Circle& c);
}  // namespace math
