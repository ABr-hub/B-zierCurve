## BézierCurve
This project offers an interactive Bézier curve visualizer using De Casteljau's algorithm. Users can add, move, or delete control points, with real-time curve updates. It includes recursive subdivision to split the curve into segments for precise approximation and compares the original with the subdivided curve.

# Bezier Curve in general & motivation [1]

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
          <img src="assets\Approx_Deg3.png" alt="Approximation of degree 3" width="600"/> 
        * 5:\
          <img src="assets\Approx_Deg5.png" alt="Approximation of degree 5" width="600"/> 
        * 10:\
          <img src="assets\Approx_Deg10.png" alt="Approximation of degree 10" width="600"/>

        &rarr; Approximation error = **Runge's phenomenon** (polynomial strives for \
        infinity but is fixed within space through given points)

        = Not all functions can be described with a simple polynomial. To \
        be able to create complex forms (e.g. for design) other approximation methods \
        need to be evaluated.


## Bezier definitions & calculation [1], [2]

*Please note that, in the following example, the control points* $P_1 = (x_1, y_1)$ *and* $P_2 = (x_1, y_1)$ \
*are positioned at the same location for visualization purposes. If these points were not* \
*overlapping, the Bézier curve would be influenced by both points individually, creating* \
*a smoother and more complex shape. However, when they are at the same spot, their* \
*combined effect results in a simplified curve segment.* 

<img src="assets\Bezier_definitions_.png" alt="Beziér definitions" width="400"/>

**Constraints**
* $(x_0, y_0)$ & $(x_3, y_3)$ are the points through which the curve has to fit
* Point(s) $(x_1, y_1)$ & $(x_2, y_2)$ controll the *gradient* at the points $(x_0, y_0)$ & $(x_3, y_3)$\
    this can be visualized as follows\
    <img src="assets\Bezier_definitions_calculation_.png" alt="Beziér definitions" width="400"/>

    &rarr; There is exactly **one** polynomial of degree 3, fullfilling these constraints \
    $p(x) = ax^3 + bx^2 + cx + d$ \
    $p'(x) = 3ax^2 + 2bx + c$ 

Together with the points $(x_0, y_0)$ & $(x_3, y_3)$ the polynomial has to fulfill:
1. $p(x_0) = y_0$ 
2. $p(x_3) = y_3$ 

Since the points $(x_1, y_1)$ & $(x_2, y_2)$ controll the gradient of the points $(x_0, y_0)$ & $(x_3, y_3)$ \
this leads to two more linear equations:

3. $p'(x_0) = \frac{y_1 - y_0}{x_1 - x_0}$ 
4. $p'(x_3) = \frac{y_3 - y_2}{x_3 - x_2}$ 


With the sample points
* $p_0 = (0.2, 0.2)$
* $p_1 = (0.5, 0.8)$
* $p_2 = (0.5, 0.8)$
* $p_3 = (0.8, 0.2)$

a solveable linear equation systen can be created to identify the coefficients of the polynomial\
aka the beziér curve: 

1. $p(x_0) = y_0 \rightarrow p(0.2) = 0.2 \rightarrow 0.2 = a(0.2)^3 + b(0.2)^2 + c(0.2) + d = 0.0008a + 0.04b + 0.2c + d$ 
2. $p(x_3) = y_3 \rightarrow p(0.8) = 0.2 \rightarrow 0.2 = ...$
3. $p'(x_0) = \frac{y_1 - y_0}{x_1 - x_0} \rightarrow = 0.2 = \frac{0.8 - 0.2}{0.5 - 0.2} \rightarrow 2 = 0.12a^2 + 0.4b + c$
4. $p'(x_0) = \frac{y_3 - y_2}{x_3 - x_2} \rightarrow = 0.2 = \frac{0.2 - 0.8}{0.8 - 0.5} \rightarrow ... $
