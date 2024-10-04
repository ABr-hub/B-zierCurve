## BézierCurve
This project offers an interactive Bézier curve visualizer using De Casteljau's algorithm. Users can add, move, or delete control points, with real-time curve updates. It includes recursive subdivision to split the curve into segments for precise approximation and compares the original with the subdivided curve.

**Repository content**
1. Usage
2. Theory

## Usage

To use the `BezierEditor` class, you can follow these steps:

1. Import the class.
2. Create an instance of the class.
3. Interact with the editor.

### Example

```python
# Import the BezierEditor class
from bezier_editor import BezierEditor

# Create an instance of the BezierEditor
editor = BezierEditor()

# Run the editor to start visualizing Bézier curves
editor.run()
```
<img src="assets\bezier_demo.gif" />

You can switch between the standard editor and the subdivision editor by passing the string \
`'sub'` when creating an instance of the class.

```python
editor = BezierEditor('sub')
```

<img src="assets\bezier_sub_demo.gif" />

When the class is initialized with control points, it allows for a direct comparison between \
the Bézier curve generated with and without subdivision in a non editable plot.

```python
editor = BezierEditor([[x1, y1], [x2, y2], [x3, y3]])
```
<img src="assets\FixedComparison.png" alt="Function to approximate" width="1000"/> 

---

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
*Please note that, in the following example, the control points* $P_1 = (x_1, y_1)$ *and* $P_2 = (x_1, y_1)$ *are positioned at the same location for visualization and generalization purposes. If these points were not overlapping, the Bézier curve would be influenced by both points individually, creating a smoother and more complex shape. However, when they are at the same spot, their combined effect results in a simplified curve segment.* 

<img src="assets\Bezier_definitions_.png" alt="Beziér definitions" width="400"/>

**Constraints**
* $(x_0, y_0)$ & $(x_3, y_3)$ are the points through which the curve has to fit
* Point(s) $(x_1, y_1)$ & $(x_2, y_2)$ controll the *gradient* at the points $(x_0, y_0)$ & $(x_3, y_3)$\
    this can be visualized as follows\
    <img src="assets\Bezier_definitions_calculation_.png" alt="Beziér definitions" width="400"/>

    &rarr; There is exactly **one** polynomial of degree 3, fullfilling these constraints
  
    *Note: Here a polynomial of degree 3 has to be evaluated since technically there are only* \
    *3 points* ($P_1 = P_2$)
  
    $p(x) = ax^3 + bx^2 + cx + d$ \
    $p'(x) = 3ax^2 + 2bx + c$ 

Together with the points $(x_0, y_0)$ & $(x_3, y_3)$ the polynomial has to fulfill:
1. $p(x_0) = y_0$ 
2. $p(x_3) = y_3$ 

Since the points $(x_1, y_1)$ & $(x_2, y_2)$ controll the gradient of the points $(x_0, y_0)$ & $(x_3, y_3)$ \
this leads to two more linear equations:

3. $p'(x_0) = \frac{y_1 - y_0}{x_1 - x_0}$ 
4. $p'(x_3) = \frac{y_3 - y_2}{x_3 - x_2}$ 


With the sample points ...
* $p_0 = (0.2, 0.2)$
* $p_1 = (0.5, 0.8)$
* $p_2 = (0.5, 0.8)$
* $p_3 = (0.8, 0.2)$

... a solveable linear equation systen can be created to identify the coefficients of the polynomial\
aka the Beziér curve: 

1. $p(x_0) = y_0 \rightarrow p(0.2) = 0.2 \rightarrow 0.2 = a(0.2)^3 + b(0.2)^2 + c(0.2) + d = 0.0008a + 0.04b + 0.2c + d$ 
2. $p(x_3) = y_3 \rightarrow p(0.8) = 0.2 \rightarrow 0.2 = ...$
3. $p'(x_0) = \frac{y_1 - y_0}{x_1 - x_0} \rightarrow = 0.2 = \frac{0.8 - 0.2}{0.5 - 0.2} \rightarrow 2 = 0.12a^2 + 0.4b + c$
4. $p'(x_0) = \frac{y_3 - y_2}{x_3 - x_2} \rightarrow = 0.2 = \frac{0.2 - 0.8}{0.8 - 0.5} \rightarrow ... $


## DeCasteljau Algorithm [3], [4]
* Used to compute a point on a Bézier curve in real applications
* Better suitable for computer calculation because numerically more stable
* Idea: Intelligent combination of straight lines returns the bezier curve


### Theory
* Linear interpolation:
    * Each step interpolates between two neighboring points (e.g. $P_0$ & $P_1$ or $P_2$ & $P_3$)
    * $P_{new}=(1-t) \cdot P_{current} + t \cdot P_{next}$
        * $P_{new}$: Point used to linearly interpolate  
        * $P_{current}$: Current controll point
        * $P_{next}$: Next controll point
        * $t$: Paramter used to determine how much of the straight line \
        between $P_{current}$ and $P_{next}$ (e.g. $\overline{P_0, P_1}$ or $\overline{P_2, P_3}$) \
        should be used \
        (This essentially influences the accuracy of the interpolated Bézier curve)

    $\Rightarrow$ This interpolation creates a new point between each neighboring \
    pair of points. This process is repeated until there is only one point left \
    on the curve.
    (How many times this interpolation has to be repeated is dependend on the \
    amout of controll points).

**Working principle**

<img src="assets\deCasteljau_AlgorithmPrinciple.gif" />


### Subdivison
Previously, the curve was generated by utilizing all control points directly. \
In the process of calculating a Bézier curve, every control point contributes \
to the final shape. The De Casteljau algorithm is applied once over a range of \
parameter values $t$ (e.g., from $0$ to $1$) to compute the curve's points.

* Simple Representation: \
  The curve is depicted as a smooth line connecting the control points, resulting \
  in a continuous shape that follows the contours defined by these points.
  
* Limited Control: \
  To alter the shape of the curve (e.g., to position it closer to or further from \
  the control points), you must manually adjust the positions of the control points.

**Bézier Curve with Recursive Subdivision:**

Segmentation: \
In recursive subdivision, the curve is divided into smaller segments. At each point $t$,\
the curve is further subdivided into two new curves until a certain depth (maximum \
recursion depth) is reached.

* More Detailed Representation: \
  This results in more points representing the curve, leading to a more detailed and \
  precise curve. The subdivision allows for better control over the shape of the curve, \
  as it brings the curve closer to the positions of the control points.

* Enhanced Customizability: \
  With recursive subdivision, the curve can be finely adjusted as needed. It provides \
  better visualization of changes in shape when the control points are moved.

**Algorithm**

The recursive subdivision algorithm breaks down a Bézier curve into smaller segments,\
which can be more easily managed or rendered. Here's how it works mathematically:

1. Subdivision at $t=0.5$: Given a set of control points $P_0,P_1,…,P_n$​, you \
   can compute the midpoints of each segment formed by these control points. The new\
    points are computed as follows:
   
   * Midpoint Calculation: \
     For $i=0,1,…,n−1$: \
        $M_i = {\Large\frac{P_i+P_{i+1}}{2}}$

     This results in a new set of control points $M_0,M_1,…,M_{n−1}​$.

2. Repeat Subdivision: The algorithm then applies the same process recursively to the \
   new control points $P_0,M_0,M_1,…,M_n−1,P_n$.

4. Base Case: The recursion continues until a certain depth is reached, or until the \
   control points are close enough that a straight line can represent them. The stopping \
   criterion can be based on:
   * A maximum recursion depth
   * The distance between the first and last control points falling below a certain threshold

---

### Sources
[1] https://lp.uni-goettingen.de/get/text/1265 \
[2] https://de.wikipedia.org/wiki/B%C3%A9zierkurve \
[2] https://de.wikipedia.org/wiki/De-Casteljau-Algorithmus \
[3] http://www.dma.ufg.ac.at/app/link/Grundlagen%3A2D-Grafik/module/13079?step=all
