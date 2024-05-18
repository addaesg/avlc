#pragma once

#include "../../utils/utils.h"
#include "../float/float.h"
#include <cmath>
namespace math {
using Angle = ft;

def toRadians(Angle degrees)->Angle;
def toDegrees(Angle radians)->Angle;


with(given hp) def fsin(Angle angle)->ft {
  ft sigma{0}, left, right;
  range(k, 0, hp) {
    left = (std::pow(-1.0, k) / std::tgamma(((k + 1) << 1)));
    right = angle ^ ((ft)((k << 1) + 1));
    sigma = sigma + left * right;
  }
  return sigma;
}

with(given hp) def fcos(Angle angle)->ft {
  ft sigma{0}, left, right;
  range(k, 0, hp) {
    left = std::pow(-1.0, k) / std::tgamma((k << 1) + 1);
    right = angle ^ ((ft)(k << 1));
    sigma = sigma + left * right;
  }
  return sigma;
}
};  // namespace math
