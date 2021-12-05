import time

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
TOWERS = ["q", "w", "e", "r", "t", "y", "a", "s", "g", "h", "l", "m"]


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


class Tower:
    def __init__(self, towerType, Location, upgradesPath1, upgradesPath2, keyBind):
        self.towerType = towerType
        self.Location = Location
        self.upgradesPath1 = upgradesPath1
        self.upgradesPath2 = upgradesPath2
        self.keyBind = keyBind

    def set_towerType(self, new_towerType):
        self.towerType = new_towerType

    def set_Location(self, new_Location):
        self.Location = new_Location

    def set_upgradesPath1(self, new_upgradesPath1):
        self.upgradesPath1 = new_upgradesPath1

    def set_upgradesPath2(self, new_upgradesPath2):
        self.upgradesPath2 = new_upgradesPath2

    def PlaceTower(self):
        pyautogui.press(self.keyBind)
        pyautogui.click(self.Location[0], self.Location[1])
        for _ in range(self.upgradesPath1):
            pyautogui.press(',')
        for _ in range(self.upgradesPath2):
            pyautogui.press('.')


# Towers can only go 3 or 4 upgrades on one path at a time, that's why some have 2 different options
lead_towers = {"Dart Monkey": ["q", 4, lambda: random.randint(0, 2)],
               "Boomerang Monkey": ["r", lambda: random.randint(0, 2), lambda: random.randint(2, 4)],
               "Bomb Shooter 1": ["y", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
               "Bomb Shooter 2": ["y", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
               "Tack Shooter": ["w", 4, lambda: random.randint(0, 2)],
               "Ice Monkey 1": ["a", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
               "Ice Monkey 2": ["a", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
               "Glue Monkey 1": ["s", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
               "Glue Monkey 2": ["s", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
               "Sniper Monkey 1": ["e", lambda: random.randint(1, 4), lambda: random.randint(0, 2)],
               "Sniper Monkey 2": ["e", lambda: random.randint(1, 2), lambda: random.randint(0, 4)],
               "Wizard Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
               "Wizard Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
               "Super Monkey": ["g", 2, lambda: random.randint(0, 4)],
               "Bloonchipper": [";", 2, lambda: random.randint(0, 4)]}

camo_towers = {"Dart Monkey": ["q", 2, lambda: random.randint(0, 4)],
               "Boomerang Monkey": ["r", 4, lambda: random.randint(0, 2)],
               "Sniper Monkey": ["e", lambda: random.randint(0, 4), 2],
               "Wizard Monkey": ["h", lambda: random.randint(0, 4), 2],
               "Ninja Monkey 1": ["t", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
               "Ninja Monkey 2": ["t", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],}


all_tower_types = {"Dart Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Dart Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Boomerang Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Boomerang Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Bomb Shooter 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Bomb Shooter 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Tack Shooter 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Tack Shooter 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Ice Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Ice Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Glue Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Glue Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Sniper Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Sniper Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Ninja Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Ninja Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Super Monkey 1": ["h", lambda: random.randint(0, 3), lambda: random.randint(0, 2)],
                   "Super Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Bloonchipper  1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Bloonchipper 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   "Wizard Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                   "Wizard Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                   }


# Each parent maybe be an array of the towers placed (or at least wants to place)
def crossover(Parent1, Parent2):
    # Not sure 100% what would be best for crossover, take a tower for each parent and swap them?
    index1 = random.randint(0, len(Parent1))
    index2 = random.randint(0, len(Parent2))
    temp1 = Parent1[index1]
    temp2 = Parent2[index2]
    Parent1[index1] = temp2
    Parent2[index2] = temp1
    return Parent1, Parent2


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
