#include "trigonometry.h"

namespace math {

def toRadians(Angle degrees)->Angle { return degrees * (Angle)0.0174533; }
def toDegrees(Angle radians)->Angle { return radians / (Angle)0.0174533; }

}  // namespace math
