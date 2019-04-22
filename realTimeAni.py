#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:18:50 2019
Chloe Johnson
ME369 Spring 2019

reference: https://matplotlib.org/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
@author: chloe
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen(t=0):
    cnt = 0
    while cnt < 500:
        cnt += 1
        t += 0.1
        yield t, -5*t


def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [],'o', lw=2)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    if y >= ymax:
        ax.set_ylim(ymin,2*ymax)
        ax.figure.canvas.draw()
    if y <= ymin:
        ax.set_ylim(2*ymin,ymax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=.001,
                              repeat=False, init_func=init)
plt.show()
