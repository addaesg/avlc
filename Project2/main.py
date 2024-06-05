from game.all import *


def main():
    (width, height) = (800, 600)
    backgroundColor = Color.BLACK
    window = Window(width, height, "Curvinha Fellas", backgroundColor)

    captions = BoxCaption()
    controlPoints = ControlPoints([], 5, Color.BLACK, captions)
    #bezierCurve = BezierCurve(controlPoints.points, Color.DARK_CYAN, 3, captions)
    #lagradgeCurve = InterpolatedCurve(controlPoints.points, Color.DARK_CYAN, 3, captions)
    monomialCurve = MonomialInterpolatedCurve(controlPoints.points, Color.DARK_GREY, 3, captions)

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