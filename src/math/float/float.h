#pragma once

#include <algorithm>
#include <cstdint>
// #include <cmath>
// #include <cstddef>

#include "../../utils/utils.h"

namespace math {

using Digits = uint32_t;

// syntatic sugar to get things from i3e float
// them/their/it/acoisa
namespace i3e {
// i3e float are biased as fuck
// they don't use two complement for exponent
// so they have an integrated bias that is subtracted from the stored exponent
// to get the real exponent and so be able to represent negative exponent
const int BIAS = 127;

// SignBit [31]
// Exponent [31...24]
// Mantissa [23...0]
def bits(float fl)->Digits;
def getExponent(float fl)->Digits;
def getMantissa(float fl)->Digits;
def getSign(float fl)->Digits;
def getMantissaAndExponent(float fl)->mkpair<both(Digits)>;
}  // namespace i3e

//
// our/we/re/tard

// mantissa_size = precision
// exponent_size = 32 - precision
with(given PRECISION = 23, given FLOAT_SIZE = 32,
     given MANTISSA_LENGHT = PRECISION,
     given EXPONENT_LENGTH = FLOAT_SIZE - (MANTISSA_LENGHT + 1),
     given MAX_EXPONENT = (1 << (EXPONENT_LENGTH - 1)) - 1,
     given MIN_EXPONENT =  -MAX_EXPONENT + 1,
     given BIAS = MAX_EXPONENT) 
class Float {
  int exponent;
  Digits sign, mantissa;

 public:
  Float() = default;

  // float -> Float
  Float(float fl) {
    // print("---------------");
    // print("Float: f -> F", fl);
    // print(bin(*(Digits*)(&fl)));
    let i3e_sign = i3e::getSign(fl);
    auto [i3e_mantissa, i3e_exponent] = i3e::getMantissaAndExponent(fl);
    {
      // sign is preserved
      sign = i3e_sign;
    }
    {
      exponent = std::clamp(((int)(i3e_exponent)-i3e::BIAS), MIN_EXPONENT,
                            MAX_EXPONENT);
    }
    {
      // normalizar a mantissa
      // usando truncagem, floor, sei la o nome dessa porra
      let mantissa_offset = 24 - MANTISSA_LENGHT;
      if (mantissa_offset < 0) {
        mantissa = i3e_mantissa << std::abs(mantissa_offset);
      } else {
        mantissa = i3e_mantissa >> mantissa_offset;
      }
    }
    let rep = i3e_sign | (i3e_exponent << 23) | i3e_mantissa;
    // print(bin(rep));
  };

  // Float -> float
  operator float() const {
    let result{0};
    Digits i3e_sign{0}, i3e_exponent{0}, i3e_mantissa{0};
    {
      i3e_sign = sign;
    }
    {
      // exponent shinanigans ihaaa
      i3e_exponent = std::clamp(exponent, -126, 127);
      i3e_exponent += i3e::BIAS - (i3e_exponent == -126);
      // shift the exponent
      i3e_exponent <<= 23;
    }
    {
      // fit the mantissa
      let mantissa_offset = (int)(24 - MANTISSA_LENGHT);
      if (mantissa_offset < 0) {
        i3e_mantissa = mantissa >> std::abs(mantissa_offset);
      } else {
        i3e_mantissa = mantissa << mantissa_offset;
      }
    }

    let rep = (uint32_t)(i3e_sign | i3e_exponent | i3e_mantissa);
    return *(float*)(&rep);
  };

  // Arithmetic operators
  def operator-()->Float { return -((float)(*this)); };

#define FloatOp(op)                         \
  def operator op(Float other)->Float {     \
    return (float)(*this) op (float)(other); \
  };
  arithmeticOperators(FloatOp);

#define FloatfloatOp(op)                    \
  def operator op(float other)->Float {     \
    return (float)(*this) op (float)(other); \
  };
  arithmeticOperators(FloatfloatOp);

  // + - * /

  // power
  def operator^(Float other)->Float {
    return std::pow((float)(*this), (float)(other));
  };
  // factorial
  def operator!()->Float { return std::tgamma((float)(*this) + 1); };
};
std::istream& operator>>(std::istream& is, Float<>& p);
std::ostream& operator<<(std::istream& os, const Float<>& p);
// using ft = Float;

}  // namespace math
#define ft math::Float<>
