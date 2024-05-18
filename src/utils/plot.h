#pragma once

#include <fstream>

#include "misc.h"

namespace plot {

using Path = std::string;

// same random thing into a file;
with(typename Thing) 
def saveToFile(Thing thing, Path filename) {
  std::ofstream file;
  file.open(filename);
  file << thing;
  file.close();
}

// Plot things, call gnu plot
// to plot sample Points
// see "src/circle.gnu"
with(typename Points) 
def plot(const Points& samples, Path script) {
  plot::saveToFile(samples, "circle.points");
  auto prompt = "gnuplot ";
  (void)system((prompt + script).c_str());
}

}  // namespace plot
