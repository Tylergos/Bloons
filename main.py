import time
import random
import pygetwindow as pgw
import pyautogui as pag
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image
import TowerTypes as TT
from Permutation import Permutation

WINDOW_HEIGHT = 0
WINDOW_WIDTH = 600
TOP_LEFT = (0, 0)
GRIDTL = (7, 30)  # left, top
GRIDBR = (561 - GRIDTL[0], 430 - GRIDTL[1])  # right, bottom
DEATHTL = (280, 180)  # left, top
DEATHBR = (405 - DEATHTL[0], 235 - DEATHTL[1])  # right, bottom


def adjust_window(name, width, height=0):
    """
    Used to adjust the size of the window
    :param name: string of the name of the window, typically "Bloons TD5"
    :param width: width in pixels of the window
    :param height: height in pixels of the window, height=0 for automatic resizing of the window
    :return: Returns the window size and top left of the window
    """
    # height = 0 results in automatic sizing based on width
    win = pgw.getWindowsWithTitle(name)[0]
    win.size = (width, height)
    win.moveTo(0, 0)
    win.activate()
    return win.size, win.topleft


def screenshot_window(width, height, name="window.png"):
    """
    Used to take a screenshot of the window, automatically titled window.png
    :param width: width in pixel of the screenshot
    :param height: height in pixel of the screenshot
    :param name: The name of the picture
    :return: reference to the image file
    """
    return pag.screenshot(name, region=(0, 0, width, height))


def screenshot_map(name="map.png"):
    """
    Takes a screenshot of the map according to the grid, automatically titled map.png
    :param name: The name of the picture
    :return: reference to the image file
    """
    return pag.screenshot(name, region=(*GRIDTL, *GRIDBR))


def screenshot_death(name="death.png"):
    """
    Takes a screenshot of the death wave counter, automatically titled death.png
    :param name: The name of the picture
    :return: reference to the image file
    """
    return pag.screenshot(name, region=(*DEATHTL, *DEATHBR))

def show_grid(img_name="map.png"):
    """
    Shows the map image with the grid overlayed onto it
    :param img_name: The name of the image file, by default map.png
    """
    im = pag.screenshot(img_name, region=(*GRIDTL, *GRIDBR))
    coords = gridify(im)
    for coord in coords:
        for x, y in coord:
            plt.scatter(x, y)
    # im = screenshot_window(WINDOW_WIDTH, WINDOW_HEIGHT)
    plt.imshow(im)
    plt.show()


def gridify(image, gridsize=48):
    """
    Takes in the image of the map and creates a grid relative to the size of the map
    :param image: The image file of the map
    :param gridsize: The size if the tiles in pixels, default is 48 as this is the largest size of monkey being used
    :return: The coordinate grid generated
    """
    # map size is 867 pixels wide
    frac = image.size[0] / 867
    cells_x = 867 // gridsize
    cells_y = int(867 * image.size[1] / image.size[0]) // gridsize
    coords = []
    for x in range(cells_x):
        tempcoord = []
        for y in range(cells_y):
            tempcoord.append((np.floor(frac * gridsize * x + gridsize/2) + GRIDTL[0], np.floor(frac * gridsize * y + gridsize/2) + GRIDTL[1]))
        coords.append(tempcoord)
    return coords


# Each parent maybe be an array of the towers placed (or at least wants to place)
def cross_swap(parent1, parent2):
    """
    Crossover that swaps a tower from each parent to the other
    :param parent1: Permutation of parent1
    :param parent2: Permutation of parent2
    :return: Permutation of parent1 and parent2
    """
    index1 = random.randint(0, len(parent1))
    index2 = random.randint(0, len(parent2))
    temp1 = parent1[index1]
    temp2 = parent2[index2]
    parent1[index1] = temp2
    parent2[index2] = temp1
    return parent1, parent2


def mut_change_tower_type(parent):
    """
    Mutation that will take a tower in a parent and replace it with a new tower.
    This new tower may be a different type and also have different amounts of upgrades.
    It will stay in the same location it was before.
    :param parent: The parent to change
    :return: Returns the changed parent
    """
    cur_tower = random.choise(parent)
    dictionary_num = random.randint(1, 3)
    if dictionary_num == 1:
        tower_index = random.randint(0, len(TT.lead_towers)-1)
        tower_type = list(TT.lead_towers.keys())[tower_index]
        upgrades1 = TT.lead_towers.get(tower_type)[1]()
        upgrades2 = TT.lead_towers.get(tower_type)[2]()
        keybind = TT.lead_towers.get(tower_type)[0]
    elif dictionary_num == 2:
        tower_index = random.randint(0, len(TT.camo_towers)-1)
        tower_type = list(TT.camo_towers.keys())[tower_index]
        upgrades1 = TT.camo_towers.get(tower_type)[1]()
        upgrades2 = TT.camo_towers.get(tower_type)[2]()
        keybind = TT.camo_towers.get(tower_type)[0]
    else:
        tower_index = random.randint(0, len(TT.all_tower_types)-1)
        tower_type = list(TT.all_tower_types.keys())[tower_index]
        upgrades1 = TT.all_tower_types.get(tower_type)[1]()
        upgrades2 = TT.all_tower_types.get(tower_type)[2]()
        keybind = TT.all_tower_types.get(tower_type)[0]
    cur_tower.set_tower_type(tower_type)
    cur_tower.set_upgrades_path1(upgrades1)
    cur_tower.set_upgrades_path2(upgrades2)
    cur_tower.set_keybind(keybind)
    return parent


def tournament_selection(selection_size, pop_size, population):
    """
    Does a tournament selection. Picks selection_size amount of permutations from population and sees which is best
    :param selection_size: The number of permutations in selection
    :param pop_size: The total size of the population
    :param population: The current population the selection is done on
    :return: The best permutation from the current population
    """
    # Similar to what was done for assignment 1 (Lucas Croslyn)
    choices = random.sample(range(0, pop_size), selection_size)
    fitnesses = []
    for i in choices:
        fitnesses.append(population[i].fitness)
    max_fitness = max(fitnesses)
    return population[fitnesses.index(max_fitness)]


def initialize(pop_size):
    """
    Makes an initial population of size pop_size
    :param pop_size: The size the population will be
    :return: The generated initial population
    """
    # Similar to what was done for assignment 1 (Lucas Croslyn)
    population = []
    for _ in range(pop_size):
        population.append(Permutation((0, 0)))
    return population


def evaluate_permutation(permutation):
    im = pag.screenshot("map.png", region=(*GRIDTL, *GRIDBR))
    im = pag.screenshot("death.png", region=(*DEATHTL, *DEATHBR))
    pag.screenshot("window.png", region=(*TOP_LEFT, *(np.add(TOP_LEFT, [WINDOW_WIDTH, WINDOW_HEIGHT]))))
    # place all the towers
    permutation.place_towers()
    while True:
        val = death_wave()
        if val != -1:
            return val
        time.sleep(5)


def death_wave():
    screenshot_death()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    test = pytesseract.image_to_string(Image.open('death.png'))
    if len(test) != 0:
        ind = test.find("Wave: ")
        if ind != -1:
            return int(test[(ind + len("Wave: "))::])
    return -1


if __name__ == '__main__':
    size, tl = adjust_window("Bloons TD5", WINDOW_WIDTH)
    WINDOW_WIDTH = size[0]
    WINDOW_HEIGHT = size[1]
    time.sleep(0.05)
    # im = pag.screenshot("map.png", region=(*GRIDTL, *GRIDBR))
    # im = pag.screenshot("death.png", region=(*DEATHTL, *DEATHBR))
    # pag.screenshot("window.png", region=(*TOP_LEFT, *(np.add(TOP_LEFT, [WINDOW_WIDTH, WINDOW_HEIGHT]))))
    # coords = gridify(im)
    val = death_wave()
    print(val)

    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # test = pytesseract.image_to_string(Image.open('death.png'))
    # # # str.replace('\f', '')
    # print(test)
