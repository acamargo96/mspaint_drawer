import os
import time

import win32gui, win32con, win32api
import pyautogui

import numpy as np

class MSPaintDrawer():

    def __init__(self):

        self.tests = Tests(self)
        self.functions = Functions()
        self.mazes = Mazes()    

        self.open_paint()

        # updates the canvas location 
        self.canvas_edge = (1403, 864)
        self.resize_canvas(x=1900, y=1000)

        self.config_coords()

        # Minimum coordinate for drawing. Maximum is the self.canvas_edge
        self.min_canvas = (5, 144)

        time.sleep(1)

    def open_paint(self):        
        
        ''' Runs the mspaint.exe and maximizes the window. '''
        os.startfile(r'C:\WINDOWS\system32\mspaint.exe')
        time.sleep(0.5)
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def resize_canvas(self, x, y):

        ''' Resizes the mspaint canvas. Infers a 1920x1080 resolution. '''
 
        pyautogui.moveTo(self.canvas_edge[0], self.canvas_edge[1])
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(x=x, y=y)
        pyautogui.mouseUp(button='left')

    def config_coords(self):

        ''' Configures dictionaries for buttons. '''
        self.tool_dict = {'pencil' : (310, 70), 'fill'   :  (335, 70),
                          'text' :   (360, 70), 'eraser' : (310, 100)}

        self.shapes_dict = {'line' :           (440, 60), 
                            'curve' :          (460, 60),
                            'ellipse' :        (480, 60), 
                            'rectangle' :      (500, 60),
                            'rounded_rect' :   (520, 60), 
                            'polygon' :        (540, 60),
                            'triangle' :       (560, 60), 
                            'right_triangle' : (440, 80),
                            'losangle' :       (460, 80),
                            'pentagon' :       (480, 80),
                            'hexagon' :        (500, 80),
                            'right_arrow' :    (520, 80),
                            'left_arrow' :     (540, 80),
                            'up_arrow' :       (560, 80),
                            'down_arrow' :     (440, 100),
                            'four_pt_star' :   (460, 100),
                            'five_pt_star' :   (480, 100),
                            'six_pt_star' :    (500, 100),
                            'rect_textbox' :   (520, 100),
                            'round_textbox' :  (540, 100),
                            'cloud_textbox' :  (560, 100)}

        self.color_selector_dict = {'color_1' : (800, 80), 
                                    'color_2' : (840, 80)}

        self.colors_dict = {'black' :           (875, 60), 
                            'white'  :          (875, 80),
                            'grey'  :           (897, 60), 
                            'light_grey' :      (897, 80),
                            'dark_red' :        (919, 60), 
                            'brown':            (919, 80),
                            'red' :             (941, 60), 
                            'pink' :            (941, 80),
                            'orange' :          (963, 60), 
                            'gold' :            (963, 80),
                            'yellow' :          (985, 60), 
                            'light_yellow' :    (985, 80),
                            'green' :           (1007, 60), 
                            'lime' :            (1007, 80),
                            'turquoise' :       (1029, 60), 
                            'light_turquoise' : (1029, 80),
                            'indigo' :          (1051, 60), 
                            'blue_grey' :       (1051, 80),
                            'purple' :          (1073, 60), 
                            'lavender' :        (1073, 80)}

    def valid_coords(self, coords):
        
        ''' Checks if the coordinate input is inside the canvas. '''
        x, y = coords
        x_cond = x >= self.min_canvas[0] and x <= self.canvas_edge[0]
        y_cond = y >= self.min_canvas[1] and y <= self.canvas_edge[1]

        return x_cond and y_cond

    def draw_simple_shape(self, shape, start, end, color):

        ''' This method is the simplest to draw shapes and is the same as a 'drag and drop'
            manual operation.
            
            Args:
            
            shape (str): the shape to be drawn.
            start (iterable): coordinates to start shape.
            end (iterable): coordinates to end shape.'''

        if shape in self.shapes_dict.keys():

            if not self.valid_coords(start):
                raise ValueError('Invalid start coordinates {}. Coordinates must be betwenn {} and {}'.format(start, self.min_canvas, self.canvas_edge))
                
            elif not self.valid_coords(end):
                raise ValueError('Invalid end coordinates {}. Coordinates must be betwenn {} and {}'.format(end, self.min_canvas, self.canvas_edge))
            
            else:
                
                # Selects color
                if color not in self.colors_dict.keys():
                    color = 'black'

                x_color, y_color = self.colors_dict[color]
                pyautogui.click(x_color, y_color)

                # clicks shape
                x, y = self.shapes_dict[shape]
                pyautogui.click(x, y)

                # moves to start
                pyautogui.moveTo(x=start[0], y=start[1])
                pyautogui.mouseDown(button='left')
                pyautogui.moveTo(x=end[0], y=end[1])
                pyautogui.mouseUp(button='left')
            
        else:
            valid_keys = '\n'.join([s] for s in list(self.shapes_dict))
            raise KeyError('Shape "{}" is invalid. Valid shapes are:\n{}'.format(shape, valid_keys))

    def draw_polygon(self, start, coords, color):

        ''' Draws a polygon with n = len(coords) vertices. '''

        if self.valid_coords(start):

            # Selects color
            if color not in self.colors_dict.keys():
                color = 'black'

            x_color, y_color = self.colors_dict[color]
            pyautogui.click(x_color, y_color)

            # Selects 'polygon' shape
            x_poly, y_poly = self.shapes_dict['polygon']
            pyautogui.click(x_poly, y_poly)

            pyautogui.moveTo(x=start[0], y=start[1])

            for c in coords:
                # iterates for all coordinates

                if self.valid_coords(c):
                    pyautogui.mouseDown(button='left')
                    pyautogui.moveTo(x=c[0], y=c[1])
                    pyautogui.mouseUp(button='left')

            # moves back to start
            pyautogui.mouseDown(button='left')
            pyautogui.moveTo(x=start[0], y=start[1])
            pyautogui.mouseUp(button='left')

        else:
            raise ValueError('Invalid start coordinates {}. Coordinates must be betwenn {} and {}'.format(start, self.min_canvas, self.canvas_edge))

    def draw_curve(self, start, end, curve_coords):
        
        print('Not yet implemented')
        # TODO: this
        ''' Draws a curve with n = len(coords) clicks to create the curvature. '''
        '''
        # draws the main line
        self.draw_simple_shape('curve', start, end)
        # clicks a point out of the canvas to deselect the curve
        pyautogui.click(x=1000, y=5)
        print('clicked')

        for c in curve_coords:
            # add curves
            pyautogui.click(x=c[0], y=c[1])

        pyautogui.click(x=1000, y=5)'''

    def draw_circle_by_r(self, start, radius, color='black'):

        ''' Different than draw_simple_shape, which doesn't calculate the circle radius. 
            
            Args:

            start (iterable): xy coordinates of the circumference center.
            radius (int) : circumference radius in pixels. '''

        if self.valid_coords(start):
            end = (start[0] + radius, start[1] + radius)
            
            if self.valid_coords(end):
                self.draw_simple_shape(shape='ellipse', start=start, end=end, color=color)
            
            else:
                valid_rs = (self.canvas_edge[0] - start[0],
                            self.canvas_edge[1] - start[1],
                            start[0] - self.min_canvas[0],
                            start[1] - self.min_canvas[1])

                max_r = max(valid_rs)
                min_r = min(valid_rs)

                raise ValueError('Invalid radius {}. Radius must be betwenn {} and {}'.format(radius, max_r, min_r))    

        else:
            raise ValueError('Invalid start coordinates {}. Coordinates must be betwenn {} and {}'.format(start, self.min_canvas, self.canvas_edge))

    def draw_pencil(self, start, coords, color='black'):

        ''' Uses the pencil to draw lines based on a coordinate list. '''

        # Selects 'pencil' tool

        if self.valid_coords(start):

            # Selects pencil tool
            x_pencil , y_pencil = self.tool_dict['pencil']
            pyautogui.click(x_pencil, y_pencil)

            # Selects color
            if color in self.colors_dict.keys():

                x_color, y_color = self.colors_dict[color]
                pyautogui.moveTo(x=x_color, y=y_color)
                pyautogui.click()
            
            elif color != 'random':
                color = 'black'

            pyautogui.moveTo(x=start[0], y=start[1])
            previous_c_valid = True
            
            for i in range(len(coords)):

                c = coords[i]
                # iterates for all coordinates

                if self.valid_coords(c):

                    if previous_c_valid:
                        
                        if color == 'random':
                            rand_color = np.random.choice(list(self.colors_dict.keys()))
                            x_color, y_color = self.colors_dict[rand_color]
                            pyautogui.moveTo(x=x_color, y=y_color)
                            pyautogui.click()

                            if i > 0:
                                pyautogui.moveTo(x=coords[i-1][0], y=coords[i-1][1])
                            else:
                                pyautogui.moveTo(x=start[0], y=start[1])

                        pyautogui.mouseDown(button='left')
                        pyautogui.moveTo(x=c[0], y=c[1])
                        pyautogui.mouseUp(button='left')

                    else:
                        # Avoids drawing a straight line between distant points
                        pyautogui.moveTo(x=c[0], y=c[1])

                    previous_c_valid = True
                
                else:
                    previous_c_valid = False

        else:
            raise ValueError('Invalid start coordinates {}. Coordinates must be betwenn {} and {}'.format(start, self.min_canvas, self.canvas_edge))


class Tests():

    def __init__(self, des):

        self.des = des

    def simple_draw(self):

        ''' Shape drawing test. '''
        for shape in self.des.shapes_dict.keys():

            if shape != 'curve' and shape != 'polygon':

                self.des.draw_simple_shape(shape=shape, start=(200, 200), end=(800, 800))
                time.sleep(0.1)

    def polygons(self):

        ''' Polygon drawing test. '''
        coords = np.mgrid[200:800:100, 200:800:100].reshape(2,-1).T
        self.des.draw_polygon((200, 200), coords)

    def pencil(self):

        ''' creates a spiral using its parametric equations:

            x(t) = a * t * cos(t)
            y(t) = a * t * sin(t) '''

        start = (300,300)
        a = 20
        t = np.deg2rad(np.arange(0, 2880, 1))
        x = a * t * np.cos(t) + start[0]
        y = a * t * np.sin(t) + start[1]

        x = x.astype(int)
        y = y.astype(int)
            
        coords = np.vstack((x,y)).T
        #print(coords)
        self.des.draw_pencil(start=start, coords=coords, color='random')

    def coords(self):
        
        ''' Tests button locations.'''

        dicts = [self.des.tool_dict, self.des.shapes_dict, self.des.color_selector_dict, self.des.colors_dict]

        for d in dicts:
            for coord in d.values():
                pyautogui.moveTo(x=coord[0], y=coord[1])
                time.sleep(2)


class Functions():

    def spiral(self, origin, a=20.0, max_angle=2880):

        ''' creates a spiral using its parametric equations:

            x(t) = a * t * cos(t)
            y(t) = a * t * sin(t) 
            
            Args:
            
            origin (iterable): (x, y) coordinates of the curve's starting point.
            a (float): equations' parameter.
            max_angle (int): maximum angle t in degrees'''

        t = np.deg2rad(np.arange(0, max_angle, 1))
        x = a * t * np.cos(t) + origin[0]
        y = a * t * np.sin(t) + origin[1]

        x = x.astype(int)
        y = y.astype(int)

        coords = np.vstack((x,y)).T

        return coords

    def sine(self, origin, max_x, a=20.0, b=5.0):

        ''' creates a sine function:

            Args:
            
            origin (iterable): (x, y) coordinates of the curve's starting point.
            max_x (int): maximum x value in degrees
            a (float): amplitude parameter.
            b (float): angle multiplier. '''

        x = np.arange(origin[0], max_x, 1)
        y = a * np.sin(b * x) + origin[1]

        x = x.astype(int)
        y = y.astype(int)

        coords = np.vstack((x,y)).T
        return coords

    def square(self, origin, side=100):

        ''' creates a square. '''
        x = origin[0]
        y = origin[1]

        coords = [origin, (x + side, y), (x + side, y + side), (x, y + side), origin]

        return coords

class Mazes():

    def square(self, origin, side=100, space_size=5):
        
        ''' Creates the coordinates to a square maze.
        
            Args:
            
            origin (iterable): (x, y) coordinates of the maze's starting point.
            side (int): initial size of the maze's side.
            space_size (int): the size of the space with which the side is reduced'''

        directions = {
            'up'    : lambda x, y, side: (x, y - side),
            'right' : lambda x, y, side: (x + side, y),
            'down'  : lambda x, y, side: (x, y + side),
            'left'  : lambda x, y, side: (x - side, y)
        }

        x = origin[0]
        y = origin[1]
        coords = [origin, (x + side, y), (x + side, y + side), (x, y + side)]
        side -= space_size

        while side > space_size:
            
            count = 0
            for d in directions.keys():
                
                if count == 2:
                    side -= space_size

                last_coord = coords[-1]
                x = last_coord[0]
                y = last_coord[1]

                func = directions[d]
                new_coord = func(x, y, side)
                coords.append(new_coord)

                count += 1

            side -= space_size

        return coords

    def triangle(self, origin, side=100, space_size=5, pointing='up'):

        ''' Creates the coordinates to an equilateral triangle maze.
        
            Args:
            
            origin (iterable): (x, y) coordinates of the maze's starting point.
            side (int): initial size of the maze's side.
            space_size (int): the size of the space with which the side is reduced.
            pointing (str): the direction ('up' or 'down') that the triangle is pointing.'''

        x = origin[0]
        y = origin[1]

        directions = {
            'up' : {
                'coords' : [
                    origin, 
                    (x + side / 2, y + side * np.sin(np.deg2rad(60))), 
                    (x - side / 2, y + side * np.sin(np.deg2rad(60)))
                ],

                'directions' : {
                    'up'    : lambda x, y, side: (x + side / 2, y - side * np.sin(np.deg2rad(60))),
                    'down'  : lambda x, y, side: (x + side / 2, y + side * np.sin(np.deg2rad(60))),
                    'left'  : lambda x, y, side: (x - side, y)
                }
            },

            'down' : {
                'coords' : [
                    origin, 
                    (x + side / 2, y - side * np.sin(np.deg2rad(60))), 
                    (x - side / 2, y - side * np.sin(np.deg2rad(60)))
                ],
                
                'directions' : {
                    'down'  : lambda x, y, side: (x + side / 2, y + side * np.sin(np.deg2rad(60))),
                    'up'    : lambda x, y, side: (x + side / 2, y - side * np.sin(np.deg2rad(60))),
                    'left'  : lambda x, y, side: (x - side, y)
                }
            }
        }

        coords = directions[pointing]['coords']
        dirs = directions[pointing]['directions']
        side -= space_size

        while side > space_size:
            
            count = 0
            for d in dirs.keys():
                
                if count > 0 :
                    side -= space_size

                last_coord = coords[-1]
                x = last_coord[0]
                y = last_coord[1]

                func = dirs[d]
                new_coord = func(x, y, side)
                coords.append(new_coord)

                count += 1

            side -= space_size

        return coords

def main():

    des = MSPaintDrawer()
    
    #square = des.functions.square(origin=(300,300))
    #sine = des.functions.sine(origin=(400,400), max_x=600, a=60, b=0.2)

    colors = [c for c in list(des.colors_dict.keys()) if c != 'white']
    space_size = 5
    # upward houses
    for i in range(len(colors[:11])):
        
        origin = (200 + 100 * i, 300)
        
        start_x_tr_1 = origin[0]
        start_y_tr_1 = origin[1]

        start_x_sq_1 = start_x_tr_1 - 50
        start_y_sq_1 = start_y_tr_1 + int(100 * np.sin(np.deg2rad(60)))

        start_x_sq_2 = start_x_sq_1
        start_y_sq_2 = start_y_sq_1 + 100

        start_x_tr_2 = origin[0]
        start_y_tr_2 = start_y_sq_2 + 100 + int(100 * np.sin(np.deg2rad(60)))

        roof_1 = des.mazes.triangle((start_x_tr_1, start_y_tr_1), side=100, space_size=space_size)
        house_1 = des.mazes.square((start_x_sq_1, start_y_sq_1), side=100, space_size=space_size)

        roof_2 = des.mazes.triangle((start_x_tr_2, start_y_tr_2), side=100, space_size=space_size, pointing='down')
        house_2 = des.mazes.square((start_x_sq_2, start_y_sq_2), side=100, space_size=space_size)

        des.draw_pencil(start=(start_x_tr_1, start_y_tr_1), coords=roof_1, color=colors[i])
        des.draw_pencil(start=(start_x_sq_1, start_y_sq_1), coords=house_1, color=colors[i])
        des.draw_pencil(start=(start_x_sq_2, start_y_sq_2), coords=house_2, color=colors[i])
        des.draw_pencil(start=(start_x_tr_2, start_y_tr_2), coords=roof_2, color=colors[i])

    # downward triangles
    
    for i in range(len(colors[:10])):
        
        origin = (250 + 100 * i, 300 + int(100 * np.sin(np.deg2rad(60))))
        
        start_x_tr_1 = origin[0]
        start_y_tr_1 = origin[1]

        start_x_tr_2 = origin[0]
        start_y_tr_2 = origin[1] + 200

        reversed_roof_1 = des.mazes.triangle((start_x_tr_1, start_y_tr_1), side=100, space_size=space_size, pointing='down')
        reversed_roof_2 = des.mazes.triangle((start_x_tr_2, start_y_tr_2), side=100, space_size=space_size, pointing='up')
        
        des.draw_pencil(start=(start_x_tr_1, start_y_tr_1), coords=reversed_roof_1, color=colors[i])
        des.draw_pencil(start=(start_x_tr_2, start_y_tr_2), coords=reversed_roof_2, color=colors[i])

    #des.draw_pencil(start=(300,300), coords=square, color='turquoise')
    #des.draw_pencil(start=(400,400), coords=sine, color='red')

    
'''
def test_curve(des):
    
    des.draw_curve((200, 200), (800, 800), ((800, 300), (800, 400)))
    des.draw_curve((400, 400), (800, 800), ((800, 300)))'''

main()

