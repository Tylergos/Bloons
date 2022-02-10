import os
import pickle
import time

from main import adjust_window, screenshot_map, gridify, next_generation, evaluate_population, show_grid

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
ELITISM = True

if __name__ == '__main__':
    POP_SIZE = 10
    SELECTION_SIZE = 3
    GENERATION_SIZE = 1
    MUT_CHANCE = 80
    CROSS_CHANCE = 15
    RUNS = 1

    default = []
    for filename in os.listdir("Saved Runs/Default"):
        file = open("Saved Runs/Tower/populations_tow2.pkl", "rb")
        reloaded_pops = pickle.load(file)
        file.close()

        size, tl = adjust_window("Bloons TD5", WINDOW_WIDTH)
        WINDOW_WIDTH = size[0]
        WINDOW_HEIGHT = size[1]
        time.sleep(0.05)
        im = screenshot_map()
        grid = gridify(im)
        for run in range(RUNS):
            all_populations = reloaded_pops
            pop = all_populations[8]
            # Make an initial population and get the fitnesses for it
            # pop = initialize(POP_SIZE)
            for gen in range(GENERATION_SIZE):
                print("Currently running gen: ", gen + 1)

                # This will make an entirely new population except for the current best permutation every 4th generation
                # if gen + 1 % 4 == 0:
                #     pop = initialize(POP_SIZE, best)

                # Calculate the new fitnesses for the population
                # Append the current population into a list which will contain all the populations.
                # After, make a new population which will have evolved from the previous
                # Repeat for how many generations wanted
                pop, best = next_generation(pop, POP_SIZE, SELECTION_SIZE, MUT_CHANCE, CROSS_CHANCE)
                evaluate_population(pop)
                all_populations.append(pop)
                print("Best this gen: wave: ", str(best.fitness), " using: ", str(best))
        #         # Saves population data after each generation
        #         file = open(filename + "Up" + str(run) + ".pkl", "wb")
        #         pickle.dump(all_populations, file)
        #         file.close()
            # show_grid()
