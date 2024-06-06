# set terminal pngcairo enhanced size 800,800
# set output 'points.png'
#
#
# set title 'Ciculu'
#
# set palette model RGB defined (1 "blue", 2 "red")
#
# plot 'circle.points' using 1:2 with points ls 1 notitle #pallete 
#
# set terminal png enhanced crop size 800,800
set terminal wxt enhanced size 800,800
set output 'points.png'
# set title 'Ciculu'
set grid
# set style line 1 lc rgb 'blue' pt 4 ps 0.5 pallete

# Define a gradient function for color
set palette defined (0 'purple', 1 'red')
stats 'circle.points' using 2 nooutput
ymin = STATS_min
ymax = STATS_max

# Read circle points and add a third column for color
# stats 'circle.points' nooutput
# num_points = STATS_records
unset colorbox

# Generate the plot with gradient colors
plot 'circle.points' using 1:2:(($2-ymin)/(ymax-ymin)) with points pt 7 ps 0.5 palette notitle
pause -1
