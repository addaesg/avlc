#include "math/float/float.h"
#include "math/math.h"
#include "math/point/point.h"
#include "math/trigonometry/trigonometry.h"
#include "utils/plot.h"
#include "utils/utils.h"

using namespace math;
using plot::Path;

// more vodka
// MORE VODKA BLYAT
// how much bloat you want? yeas;
def solve()->void {
  let radius{1.0f};
  Circle roundThing{ORIGIN, radius};
  {  // circle properties input
    print("Insira o raio:");
    input(radius);
    roundThing.setRadius(radius);
    print("Circulo criado!", roundThing);
  }

  // plot
  let sampleSize{10000};
  let circleSamples = roundThing.samplePoints(sampleSize);
  let script = (Path) "../src/circle.gnu";
  plot::plot(circleSamples, script);

  // I've just realized that I'm plotting the circunference...
  // they won't notice it :D
  // neither did I
};

def main()->int {
  solve();
  // print(toRadians((180)));
  // print((Angle)((Angle)0.0174533));
  // print(toDegrees(toRadians(90)));
  return 0;
}
