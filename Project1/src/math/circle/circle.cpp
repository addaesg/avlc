#include "circle.h"

#include <cmath>

namespace math {
// get points on the circunference
def Circle::samplePoints(ull sampleCount) const->Points {
  Points samples;
  let circle = (*this);
  // add center
  samples.push_back(circle.center());

  let sampleCircunference = [](let circle, let sampleCount) -> Points {
    Points circunference;
    constexpr int terms{10};

    Angle unitAngle = math::toRadians(360.0 / sampleCount);
    range(sample, 0, sampleCount) {
      Angle angle = sample * unitAngle;
      Point samplePoint =
          circle.radius() * (Point){fsin<terms>(angle), fcos<terms>(angle)};
      circunference.push_back(samplePoint);
    };

    return circunference;
  };

  Points circunference = sampleCircunference(circle, sampleCount);
  samples.insert(samples.end(), all(circunference));

  return samples;
};

// Print sintax sugar for point
std::ostream& operator<<(std::ostream& os, const Circle& c) {
  os << "{ Center: "
     << "[" << c.center().x << ", " << c.center().y << "] | "
     << "Radius: " << c.radius() << "}";
  return os;
}

std::istream& operator>>(std::istream& is, Circle& c) {
  Point center;
  ull radius;

  is >> center >> radius;
  c.setCenter(center);
  c.setRadius(radius);

  return is;
}

}  // namespace math
