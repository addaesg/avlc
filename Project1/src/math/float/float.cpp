#include "float.h"

namespace math {

namespace i3e {

// raw bits from float, bypass implicit conversion
// SignBit [31]
// Exponent [31...24]
// Mantissa [23...0]
def inline bits(float fl)-> Digits { return *(Digits*)(&fl); }

def getExponent(float fl)->Digits {
  let exponentMask = ((-1U) << (8)) & ~(1 << 31);
  let raw = bits(fl);
  let exponent = raw & exponentMask;
  // adjust mantissa padding
  exponent >>= 23;
  
  return exponent;
};
def getMantissa(float fl)->Digits {
  let mantissa_mask = ~(-1U << 23);
  let raw = bits(fl);
  return raw & mantissa_mask;
};

def getSign(float fl)->Digits {
  let raw = bits(fl);
  return (raw & (1 << 31));
};

def getMantissaAndExponent(float fl)->mkpair<both(Digits)> {
  return {getMantissa(fl), getExponent(fl)};
}

};  // namespace i3e
//
// Input sintax sugar for point
std::istream& operator>>(std::istream& is, Float<>& p) {
  is >> p;
  return is;
}

// Print sintax sugar for points
std::ostream& operator<<(std::ostream& os, const Float<>& ps) {
  os << ps;
  return os;
}
}  // namespace math
