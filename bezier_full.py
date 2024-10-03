# -*- coding: utf-8 -*-
# @Author: Philipp N. Mueller
# @Date:   2024-10-03 11:51:39
# @Last Modified by:   Philipp N. Mueller
# @Last Modified time: 2024-10-03 12:31:53


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton


def de_casteljau(control_points, t):
    '''
    Parameters
    ----------
    control_points (list) : List of points / coodinates representing
        the control points of the Bézier curve
    t (np.ndarray) : Represents the points between two neighbour control_points
        used to derive the linear interpolation of a point on the bézier curve
    '''
    # Get points from the plot
    points = np.array(control_points)

    # Get number of control points
    n = len(points)
    
    # De Casteljau's algorithm step by step
    for _ in range(1, n):

        # Interpolate between two neighbour controll points
        # t can be visualized e.g. as the distance taken on the
        #   linear line from one controll point to its neighbour.
        
        #   Another interpretation is the even spacing of the line 
        #   between two control points in t increments which are then used
        #   to calculate the bézier points. 
        #   
        #   Basically it influences the accuracy of the resulting bézier
        #   curve.
        # 
        # Interpolation between two points done with the following formula
        #   P_new = (1-t) * P_current + t * P_next
        points = (1 - t) * points[:-1] + t * points[1:]

    return points[0]


# Function to compute the Bézier curve
def bezier_curve(control_points, num_points=100):
    '''
    control_points (list) : list of control_points (x, y - coordinates)  
    num_points (int) : amount of t parameter values; Influences the 
        approximation accuracy 
    '''
    # Equally space the t parameter (basically the the straight line)
    # between two control points
    t_values = np.linspace(0, 1, num_points)

    # Use the de_casteljau function together with the control_points and t values
    # to calculate the curve points 
    curve_points = [de_casteljau(control_points, t) for t in t_values]

    return np.array(curve_points)


# Subdivide the Bézier curve at t = 0.5
def subdivide_bezier(control_points):
    '''
    Splits the Bézier curve at the points t=0.5 to generate two "new" curves.
    With the deCasteljau method two new sets of control points are generated which
    represent the control points of the two "new" curves.
    
    Parameters
    ----------
    control_points (list) : Coordinates of the clicked control points. 
    
    Returns
    -------
    left (list) : Control points of left curve
    righ (list) : Control points of right curve
    '''
    
    # Initialize two lists with the outer control points (origin control points)
    left = [control_points[0]]  # First point of the left curve 
    right = [control_points[-1]]  # Last point of the right curve
    points = np.array(control_points)
    
    # Interate over the linear connection of control points until only one (the
    # of the Bézier curve) is left 
    while len(points) > 1:
        # DeCasteljau algorithm with fixed t = 0.5
        points = (1 - 0.5) * points[:-1] + 0.5 * points[1:]
        
        left.append(points[0])
        right.append(points[-1])
    
    return left, right[::-1]


# Recursive subdivision to approximate the Bézier curve
def recursive_subdivision(control_points, depth, curve_points, max_depth):
    '''
    Approximate Bézier curve until max_depth is reached. During each iteration 
    two "new" curves are generated which are in turn split again until max_depth
    is reached.
    
    Parameters
    ----------
    control_points (list) : Original control points
    depth (int) : Current recursion depth (or iteration)
    max_depth (int) : Maximmum recursion depth (or number of iterations)
    curve_points (list) : Contains the control points of the splitted curves
    '''
    if depth >= max_depth:
        control_points = np.array(control_points)
        curve_points.extend(control_points)  # Add all control points of the curve
        return
    
    left, right = subdivide_bezier(control_points)
    
    # Recursively subdivide the left and right curves
    recursive_subdivision(left, depth + 1, curve_points, max_depth)
    recursive_subdivision(right, depth + 1, curve_points, max_depth)


# Interactive control of points
class BezierEditor:
    def __init__(self, type=None, control_points=None):
        
        if control_points == None:
            # To start the plotter without (None) or with subdivision (sub)
            self.type = type
            
            # Initialize base values
            self.control_points = []  # List of control points, taken from the plot
            self.selected_point = None
            self.dragging = False

            # Create blank figure
            self.figure, self.ax = plt.subplots()

            # Without subdivision
            if self.type == None:
                # Set variables containing the coordinates of the bézier curve and control polygon
                self.line, = self.ax.plot([], [], 'r-', label="Bézier Curve")   # Bézier curve
                self.control_polygon, = self.ax.plot([], [], 'bo-', label="Control Polygon")  # Control polygon

            # With subdivision
            else:
                # Set variables containing the coordinates of the bézier curve and control polygon
                # (Here the task1 which works without subdivision is included for comparison)
                self.old_curve_line, = self.ax.plot([], [], 'r-', label="Old Bézier Curve (No Subdivision)")  # Old curve in red
                self.new_curve_line, = self.ax.plot([], [], 'g-', label="New Bézier Curve (Subdivision)")  # New curve in green
                self.subdivision_polygons, = self.ax.plot([], [], 'b--', label="Subdivision Control Polygon")  # Subdivided control polygons
                self.control_polygon, = self.ax.plot([], [], 'bo-', label="Control Polygon")  # Control polygon
            
            # Figure specifications
            self.ax.set_title("Bézier Curve Editor (Left-click: Add, Right-click: Delete, Drag: Move)")
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.set_aspect('equal', adjustable='box')
            self.ax.legend()
            self.ax.grid()

            # Connect callback funtions to the event manager 
            # First argument contains the predefined event, second the referenced cb-function
            # https://matplotlib.org/stable/users/explain/figure/event_handling.html for
            # reference
            self.cid_click = self.figure.canvas.mpl_connect('button_press_event', self.on_click)
            self.cid_move = self.figure.canvas.mpl_connect('motion_notify_event', self.on_move)
            self.cid_release = self.figure.canvas.mpl_connect('button_release_event', self.on_release)

        
        else:
            try: 
                # Set up control points for the Bézier curve
                control_points = control_points

                # Generate Bézier curve points without subdivision
                curve_without_subdivision = bezier_curve(control_points)

                # Generate Bézier curve points with recursive subdivision
                curve_with_subdivision = []
                recursive_subdivision(control_points, 0, curve_with_subdivision, 3)
                curve_with_subdivision = np.array(curve_with_subdivision)


                # Plotting
                plt.figure(figsize=(10, 5))

                # Plot Bézier curve without subdivision
                plt.subplot(1, 2, 1)
                plt.plot(curve_without_subdivision[:, 0], curve_without_subdivision[:, 1], 'r-', label='Bézier Curve (No Subdivision)')
                plt.plot(control_points[0][0], control_points[0][1], 'bo')  # Start point
                plt.plot(control_points[1][0], control_points[1][1], 'bo')  # Control point
                plt.plot(control_points[2][0], control_points[2][1], 'bo')  # End point
                plt.title('Bézier Curve Without Subdivision')
                plt.xlim(-0.1, 1.1)
                plt.ylim(-0.1, 1.1)
                plt.grid()
                plt.legend()

                # Plot Bézier curve with recursive subdivision
                plt.subplot(1, 2, 2)
                plt.plot(curve_with_subdivision[:, 0], curve_with_subdivision[:, 1], 'g-', label='Bézier Curve (With Subdivision)')
                plt.plot(control_points[0][0], control_points[0][1], 'bo')  # Start point
                plt.plot(control_points[1][0], control_points[1][1], 'bo')  # Control point
                plt.plot(control_points[2][0], control_points[2][1], 'bo')  # End point
                plt.title('Bézier Curve With Subdivision')
                plt.xlim(-0.1, 1.1)
                plt.ylim(-0.1, 1.1)
                plt.grid()
                plt.legend()

                plt.tight_layout()
                plt.show()
            
            except:
                print('Please provide n controlpoints in the following format: [[x1, y1], [x2, y2], [,x3, y3], ...]')
            


    ## Callbackfunctions for event handling
    # Per definition each cb function has to include an event argument.
    # The possible events that can be connected to are predefined from matplotlib.

    # Click event (add or delete point, or start dragging)
    def on_click(self, event):

        # Mouse click not on canvas
        if event.inaxes != self.ax:
            return

        # Left mouse button click-event (add point, drag point)
        if event.button is MouseButton.LEFT:

            # Check if there are any points, otherwise add the first point
            if len(self.control_points) > 0:

                # Check if a point is selected for dragging
                distances = np.linalg.norm(np.array(self.control_points) - [event.xdata, event.ydata], axis=1)
                
                # If distance is close enough,....
                if distances.min() < 0.05:

                    # ... select closest point ...
                    self.selected_point = np.argmin(distances)

                    # ... and set dragging variable to true.
                    self.dragging = True
                
                else:
                    # Add a new control point if no point is selected
                    self.control_points.append([event.xdata, event.ydata])
            
            else:
                # Add the first point
                self.control_points.append([event.xdata, event.ydata])


        # Right mouse button click-event (remove point)
        elif event.button is MouseButton.RIGHT:

            # Find the closest control point to delete
            if len(self.control_points) > 0:
                
                # Get nearest point to click event
                distances = np.linalg.norm(np.array(self.control_points) - [event.xdata, event.ydata], axis=1)
                nearest_point = np.argmin(distances)
                
                # Delete if close enough
                if distances[nearest_point] < 0.05:
                    del self.control_points[nearest_point]

        # Update plot with the events
        self.update_plot()


    # Mouse move event (move point if dragging)
    def on_move(self, event):

        # Variables self.dragging and self.selected_point are set in the on_click function
        # (Resetted in the on_release function)
        if self.dragging and self.selected_point is not None:

            # Not on canvas
            if event.inaxes != self.ax:
                return

            # Update the selected control point's position
            self.control_points[self.selected_point] = [event.xdata, event.ydata]

            # Update plot with the new position of the selected points
            self.update_plot()


    # Mouse button release event (stop dragging)
    def on_release(self, event):

        # Reset variables when dragging is finished 
        self.dragging = False
        self.selected_point = None


    # Update plot after adding, deleting, or moving points
    def update_plot(self):

        # Without subdivision
        if self.type == None:
            # Plot bezier_curve 
            if len(self.control_points) >= 2:
                # Compute Bézier curve
                bezier_points = bezier_curve(self.control_points)

                # Plot bezier_points
                self.line.set_data(bezier_points[:, 0], bezier_points[:, 1])
            else:
                self.line.set_data([], [])

        # With subdivision
        else:
            # Plot bezier_curve 
            if len(self.control_points) >= 2:
                # Compute old Bézier curve
                old_curve_points = bezier_curve(self.control_points)
                
                # Plot bezier_points
                self.old_curve_line.set_data(old_curve_points[:, 0], old_curve_points[:, 1])

                # Compute new Bézier curve (with subdivision)
                new_curve_points = []
                recursive_subdivision(self.control_points, 0, new_curve_points, 5) # Set depth to 5 as intended
                new_curve_points = np.array(new_curve_points)
                self.new_curve_line.set_data(new_curve_points[:, 0], new_curve_points[:, 1])

                # # Plot bezier_points (with subdivision)
                left, right = subdivide_bezier(self.control_points)
                subdivision_polygon_points = np.array(left + right)
                self.subdivision_polygons.set_data(subdivision_polygon_points[:, 0], subdivision_polygon_points[:, 1])

        # Update control polygon
        control_points = np.array(self.control_points)

        # Set control points
        if control_points.size > 0:

            # control_points[:, 0] = x values; control_points[:, 1] = y values
            self.control_polygon.set_data(control_points[:, 0], control_points[:, 1])

        # No control points yet
        else:
            self.control_polygon.set_data([], [])
        
        # Draw canvas
        self.figure.canvas.draw()

# Run the Bézier editor
if __name__ == '__main__':
    editor = BezierEditor(control_points=[[0, 0], [0.5, 1], [1, 0]])
    plt.show()
