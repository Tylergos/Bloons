import pickle
import time
import random
import pygetwindow as pgw
import pyautogui as pag
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image, ImageOps
import TowerTypes as TT
from Permutation import Permutation
import re
import copy

WINDOW_HEIGHT = 0
WINDOW_WIDTH = 600
TOP_LEFT = (0, 0)
GRIDTL = (7, 30)  # left, top
GRIDBR = (561 - GRIDTL[0], 430 - GRIDTL[1])  # right, bottom
DEATHTL = (260, 170)  # left, top
DEATHBR = (405 - DEATHTL[0], 235 - DEATHTL[1])  # right, bottom
MONEYTL = (590, 50)  # left, top
MONEYBR = (640 - MONEYTL[0], 65 - MONEYTL[1])  # right, bottom
CANCEL_COORDS = (620, 50)


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
    im = pag.screenshot(name, region=(*DEATHTL, *DEATHBR))
    # Image is made grey scale so tesseract can read it better
    im = im.convert('L')
    im.save(name)
    return im


def screenshot_money(name="money.png"):
    """
    Takes a screenshot of the death wave counter, automatically titled money.png
    :param name: The name of the picture
    :return: reference to the image file
    """
    im = pag.screenshot(name, region=(*MONEYTL, *MONEYBR))
    # Image is made grey scale so tesseract can read it better
    im = im.convert('L')
    im.save(name)
    return im


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


def cross_swap(parent1, parent2):
    """
    Crossover that swaps a tower from each parent to the other
    :param parent1: Permutation of parent1
    :param parent2: Permutation of parent2
    :return: Permutation of parent1 and parent2
    """
    index1 = random.randint(0, len(parent1.towers_wanted)-1)
    index2 = random.randint(0, len(parent2.towers_wanted)-1)
    temp1 = parent1.towers_wanted[index1]
    temp2 = parent2.towers_wanted[index2]
    parent1.towers_wanted[index1] = temp2
    parent2.towers_wanted[index2] = temp1
    return parent1, parent2


def mut_change_tower_type(parent):
    """
    Mutation that will take a tower in a parent and replace it with a new tower.
    This new tower may be a different type and also have different amounts of upgrades.
    It will stay in the same location it was before.
    :param parent: The parent to change
    :return: Returns the changed parent
    """
    # Gets the towers which will be changed into a different one
    cur_tower = random.choice(parent.towers_wanted)
    # Multiple categories for the towers depending on if they have a specialization or not.
    # Generic category which has everything, camo category for towers which can see camo
    # and a lead category for towers which can destroy lead
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
    # Change the different parameters for the tower which was changed
    cur_tower.set_tower_type(tower_type)
    cur_tower.set_upgrades_path1(upgrades1)
    cur_tower.set_upgrades_path2(upgrades2)
    cur_tower.set_keybind(keybind)
    return parent


def mut_change_location(parent):
    cur_tower = random.choice(parent)
    cur_tower.set_location(random.choice(random.choice(grid)))


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
    return copy.deepcopy(population[fitnesses.index(max_fitness)])


def initialize(pop_size, grid):
    """
    Makes an initial population of size pop_size
    :param pop_size: The size the population will be
    :return: The generated initial population
    """
    # Similar to what was done for assignment 1 (Lucas Croslyn)
    population = []
    for _ in range(pop_size):
        population.append(Permutation(grid, CANCEL_COORDS))
    return population


def evaluate_permutation(permutation):
    """
    Runs the game on the current towers for the permutation being evaluated
    :param permutation: The current towers that will be evaluated to see which round they get to
    :return: Returns which round the towers managed to get to before dying
    """
    # place all the towers
    permutation.place_towers()
    # starts the match and speeds up
    pag.press('space', presses=2)
    while True:
        # Waits until the game over screen appears to read which round died on
        val = death_wave()
        if val != -1:
            return val
        time.sleep(5)


def evaluate_population(population):
    """
    This will update the fitness for each permutation
    :param population: The current population that will be evaluated
    :return: Not important as the function just needs to change the fitness for each permutation
    """
    for permutation in population:
        permutation.fitness = evaluate_permutation(permutation)
        # Restarts the game and waits to load the map
        pag.click(300, 300)
        time.sleep(3)
    return 0


# return wave as well for comparisons
def evaluate_permutation_towers(permutation, wave_mod=1, tower_mod=1):
    permutation.place_towers()
    while True:
        val = death_wave()
        if val != -1:
            break
        time.sleep(5)
    if wave_mod == 0 or tower_mod == 0:
        raise ValueError("wave_mod or tower_mod is zero")
    else:
        return val // wave_mod - permutation.towers_wanted // tower_mod


def evaluate_permutation_money(permutation, wave_mod=1, money_mod=0.01):
    permutation.place_towers()
    money = check_money()
    while True:
        val = death_wave()
        if val != -1:
            break
        time.sleep(5)
    if wave_mod == 0 or money_mod == 0:
        raise ValueError("wave_mod or tower_mod is zero")
    else:
        return val // wave_mod - money // money_mod


def death_wave():
    """
    Takes a screenshot of the death area to see if the death screen popped up.
    Pytesseract will read that screenshot to see if it can read any words, if it can that means the death screen appeared.
    :return: The wave numbered that the game died on
    """
    screenshot_death()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # The config makes it so tesseract will only have those characters to match to.
    # Had issue with round 40 reading as #0 before
    text = pytesseract.image_to_string(Image.open('death.png'), config="-c tessedit_char_whitelist=0123456789aevW:' '")
    if len(text) != 0:
        ind = text.find("Wave: ")
        if ind != -1:
            # Gets only the text after 'Wave: ' which will be the round counter
            re.sub('[^A-Za-z0-9]+', '', text)
            return int(text[(ind + len("Wave: "))::])
    return -1


def next_generation(cur_population, pop_size, selection_size, mutation_chance, crossover_chance):
    """
    This will do all the GA stuff like selection, mutation and crossover
    :param cur_population: The current population before any changes
    :param pop_size: The size of the population
    :param selection_size: The size of the selection, tournament style
    :param mutation_chance: The chance for a mutation to occur on a single parent.
    :param crossover_chance: The chance for a crossover to happen on the two parents
    :return: The new population after all the changes. Will be the same size as the old population
    """
    new_poulation = []
    while len(new_poulation) < pop_size:
        parent1 = tournament_selection(selection_size, pop_size, cur_population)
        parent2 = tournament_selection(selection_size, pop_size, cur_population)
        if random.randint(0, 100) < mutation_chance:
            if random.randint(0, 100) < 75:
                mut_change_location(parent1)
            else:
                mut_change_tower_type(parent1)
        if random.randint(0, 100) < mutation_chance:
            if random.randint(0, 100) < 75:
                mut_change_location(parent2)
            else:
                mut_change_tower_type(parent2)
        if random.randint(0, 100) < crossover_chance:
            parent1, parent2 = cross_swap(parent1, parent2)
        new_poulation.extend([parent1, parent2])
    return new_poulation


def check_money():
    """
    Takes a screenshot of the money area to detect the money
    Pytesseract will read that screenshot to see what the money value is
    :return: The the amount of money remaining
    """
    screenshot_death()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # The config makes it so tesseract will only have those characters to match to.
    text = pytesseract.image_to_string(Image.open('money.png'),
                                       config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:' '")
    if len(text) != 0:
        return int(text)
    return -1


if __name__ == '__main__':
    POP_SIZE = 2
    SELECTION_SIZE = 2
    GENERATION_SIZE = 2
    MUT_CHANCE = 70
    CROSS_CHANCE = 30

    size, tl = adjust_window("Bloons TD5", WINDOW_WIDTH)
    WINDOW_WIDTH = size[0]
    WINDOW_HEIGHT = size[1]
    time.sleep(0.05)
    im = screenshot_map()
    grid = gridify(im)


    all_populations = []
    # Make an initial population and get the fitnesses for it
    pop = initialize(POP_SIZE, grid)
    evaluate_population(pop)
    for _ in range(GENERATION_SIZE):
        # Append the current population into a list which will contain all the populations.
        # After, make a new population which will have evolved from the previous
        # Calculate the new fitnesses for that new population
        # Repeat for how many generations wanted
        all_populations.append(pop)
        pop = next_generation(pop, POP_SIZE, SELECTION_SIZE, MUT_CHANCE, CROSS_CHANCE)
        evaluate_population(pop)
    # show_grid()
    file = open("populations.pkl", "wb")
    pickle.dump(all_populations, file)
    file.close()





