# BézierCurve
This project offers an interactive Bézier curve visualizer using De Casteljau's algorithm. Users can add, move, or delete control points, with real-time curve updates. It includes recursive subdivision to split the curve into segments for precise approximation and compares the original with the subdivided curve.

# Bezier Curve in general [1]

* Type of spline
    * Idea of spline: Approximate a curve with many points via multiple curves of \
    few points for better fitting \
       <img src="assets\Bezier&Spline.png" alt="Function to approximate" width="400"/> 
    * Key factors are the global sides of the curve and the "connections"
    * Used to describe complex free-form curves (e.g. for complex vehicle design)

    **Why do we need that?**

    * Given function: \
       <img src="assets\Function_to_approximate_.png" alt="Function to approximate" width="600"/> \
    &rarr; Now chose any number of points (e.g. 3, 5, 10; This will also be the degree \
    of the fitting polynomial) to fit a polynom and approximate the function

        * 3: \
          <img src="assets\Approx_Deg3.png" alt="Approximation of degree 3" width="600"/> \
        * 5:\
          <img src="assets\Approx_Deg5.png" alt="Approximation of degree 5" width="600"/> \
        * 10:\
          <img src="assets\Approx_Deg10.png" alt="Approximation of degree 10" width="600"/> \

        &rarr; Approximation error = **Runge's phenomenon** (polynomial strives for \
        infinity but is fixed within space through given points)

        = Not all functions can be described with a simple polynomial. To \
        be able to create complex forms (e.g. for design) other approximation methods \
        need to be evaluated.
