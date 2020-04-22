''' author: samuel tenka
    change: 2020-04-22 
    create: 2020-04-22 
    descrp: render shaky lines and circles
'''

import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import circle, circle_perimeter_aa, line_aa

tau = 2*np.pi
costau = lambda x: np.cos(tau*x)  
sintau = lambda x: np.sin(tau*x)  

black = (0.0, 0.0, 0.0)
red   = (0.8, 0.2, 0.2)
green = (0.2, 0.8, 0.2)
blue  = (0.2, 0.2, 0.8)
gold  = (0.9, 0.7, 0.0)

def draw_line(img, row_s, col_s, row_e, col_e, color):
    ''' render an anti-aliased line onto img, an np array ''' 
    row_s, col_s, row_e, col_e = map(int, (row_s, col_s, row_e, col_e))
    expanded_color = np.expand_dims(np.expand_dims(np.array(color), 0), 0)
    rr, cc, val = line_aa(row_s, col_s, row_e, col_e)
    img[rr, cc, :] = img[rr, cc, :] + np.expand_dims(val, 2) * (
        expanded_color - img[rr, cc, :]
    )

def draw_circle_shaky(img, row_c, col_c, rad, color, dt=0.05, shake=0.05, bend=0.05):
    dl = shake * tau*rad * dt 
    row_sin = bend * rad * np.random.randn()
    col_sin = bend * rad * np.random.randn()
    row_cos = bend * rad * np.random.randn()
    col_cos = bend * rad * np.random.randn()

    t0 = 2*np.random.random()

    row = row_c + rad*costau(t0) + dl*np.random.randn() + row_sin * sintau(t0/2) + row_cos * costau(t0/2)
    col = col_c + rad*sintau(t0) + dl*np.random.randn() + col_sin * sintau(t0/2) + col_cos * costau(t0/2)
    for t in np.arange(t0+0.0, t0+1.0, dt):
        new_row = row_c + rad*costau(t+dt) + dl*np.random.randn() + row_sin * sintau((t+dt)/2) + row_cos * costau((t+dt)/2)
        new_col = col_c + rad*sintau(t+dt) + dl*np.random.randn() + col_sin * sintau((t+dt)/2) + col_cos * costau((t+dt)/2)
        draw_line(img, row, col, new_row, new_col, color)
        row = new_row
        col = new_col

def draw_line_shaky(img, row_s, col_s, row_e, col_e, color, dt=0.05, shake=0.05, bend=0.05):
    l = ((row_e-row_s)**2+(col_e-col_s)**2)**0.5

    dl = shake * l * dt 
    row_l = bend * l * np.random.randn()
    col_l = bend * l * np.random.randn()

    row = row_s + dl*np.random.randn() 
    col = col_s + dl*np.random.randn() 
    for t in np.arange(0.0, 1.0, dt):
        new_row = row_s + (t+dt)*(row_e-row_s) + dl*np.random.randn() + row_l * np.sin((t+dt)*3.14159)
        new_col = col_s + (t+dt)*(col_e-col_s) + dl*np.random.randn() + col_l * np.sin((t+dt)*3.14159)
        draw_line(img, row, col, new_row, new_col, color)
        row = new_row
        col = new_col

def draw(filename, h=256, w=256): 
    img = np.ones((h, w, 3), dtype=np.float32)
    draw_circle_shaky(img, h*0.2, w*0.5, rad=36, color=green)
    draw_circle_shaky(img, h*0.5, w*0.5, rad=36, color=red)
    draw_circle_shaky(img, h*0.8, w*0.5, rad=36, color=gold)

    draw_line_shaky(img, h*0.2, h*0.1, w*0.4, w*0.9, color=red)
    draw_line_shaky(img, h*0.7, h*0.1, w*0.8, w*0.9, color=green)
    draw_line_shaky(img, h*0.7, h*0.1, w*0.8, w*0.9, color=gold)
    plt.imsave(filename, img)

nm = 'hey.png'
draw(filename=nm)

