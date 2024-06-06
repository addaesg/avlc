from game.all import *


def main():
    (width, height) = (1200, 600)
    backgroundColor = Color.BLACK
    window = Window(width, height, "Curvinha Fellas", backgroundColor)

    captions = BoxCaption()
    controlPoints = ControlPoints([], 5, Color.BLACK, captions)
    thickness = 3
    sample_ratio = 0.2
    monomialCurve = MonomialInterpolatedCurve(controlPoints.points, Color.DARK_GREY, 
                                              thickness, captions, sample_ratio)

    while window.is_open():
        events = window.pool_events()
        controlPoints.handle_events(events)
        
        #window.draw(bezierCurve)
        #window.draw(lagradgeCurve)
        window.draw(monomialCurve)


        window.draw(controlPoints)
        window.draw(captions)
        window.update()    
    

if __name__ == "__main__":
    main()