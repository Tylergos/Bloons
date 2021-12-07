import time
import random
import pygetwindow as pgw
import pyautogui as pag
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image

WINDOW_HEIGHT = 0
WINDOW_WIDTH = 600
TOP_LEFT = (0, 0)
GRIDTL = (7, 30)  # left, top
GRIDBR = (561 - GRIDTL[0], 430 - GRIDTL[1])  # right, bottom


def adjust_window(name, width, height=0):
    # height = 0 results in automatic sizing based on width
    win = pgw.getWindowsWithTitle(name)[0]
    win.size = (width, height)
    win.moveTo(0, 0)
    win.activate()
    return win.size, win.topleft


def screenshot_window(width, height):
    return pag.screenshot("window.png", region=(0, 0, width, height))


def screenshot_map():
    return pag.screenshot("map.png", region=(*GRIDTL, *GRIDBR))


def show_grid():
    im = pag.screenshot("map.png", region=(*GRIDTL, *GRIDBR))
    coords = gridify(im)
    for coord in coords:
        for x, y in coord:
            plt.scatter(x, y)
    # im = screenshot_window(WINDOW_WIDTH, WINDOW_HEIGHT)
    plt.imshow(im)
    plt.show()


def gridify(image, gridsize=48):
    frac = image.size[0] / 867
    cells_x = 867 // gridsize
    cells_y = int(867 * image.size[1] / image.size[0]) // gridsize
    coords = []
    for x in range(cells_x):
        tempcoord = []
        for y in range(cells_y):
            tempcoord.append((np.floor(frac * gridsize * x + gridsize/2), np.floor(frac * gridsize * y + gridsize/2)))
        coords.append(tempcoord)
    return coords


def place_tower(grid, x, y, key):
    pag.press(key)
    pag.click((grid[x][y][0] + GRIDTL[0], grid[x][y][1] + GRIDTL[1]))
    # have some way of ensuring tower is removed from cursor if not successfully  placed


if __name__ == '__main__':
    # size, tl = adjust_window("Bloons TD5", WINDOW_WIDTH)
    # WINDOW_WIDTH = size[0]
    # WINDOW_HEIGHT = size[1]
    # time.sleep(0.05)
    # im = pag.screenshot("map.png", region=(*GRIDTL, *GRIDBR))
    # pag.screenshot("window.png", region=(*TOP_LEFT, *(np.add(TOP_LEFT, [WINDOW_WIDTH, WINDOW_HEIGHT]))))
    # coords = gridify(im)
    # place_tower(coords, 0, 0, TOWERS[0])
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    test = pytesseract.image_to_string(Image.open('Capture.PNG'))
    str.replace('\f', '')
