from Tower import Tower
import random
import TowerTypes as TT


def pick_tower():
    """
    This function will choose a tower type and the amount of upgrades for it
    :return: Returns the tower's type, the upgrades amount and the keybinding for the tower
    """
    dictionary_num = random.randint(1, 3)
    if dictionary_num == 1:
        tower_index = random.randint(0, len(TT.lead_towers) - 1)
        tower_type = list(TT.lead_towers.keys())[tower_index]
        upgrades1 = TT.lead_towers.get(tower_type)[1]()
        upgrades2 = TT.lead_towers.get(tower_type)[2]()
        keybind = TT.lead_towers.get(tower_type)[0]
    elif dictionary_num == 2:
        tower_index = random.randint(0, len(TT.camo_towers) - 1)
        tower_type = list(TT.camo_towers.keys())[tower_index]
        upgrades1 = TT.camo_towers.get(tower_type)[1]()
        upgrades2 = TT.camo_towers.get(tower_type)[2]()
        keybind = TT.camo_towers.get(tower_type)[0]
    else:
        tower_index = random.randint(0, len(TT.all_tower_types) - 1)
        tower_type = list(TT.all_tower_types.keys())[tower_index]
        upgrades1 = TT.all_tower_types.get(tower_type)[1]()
        upgrades2 = TT.all_tower_types.get(tower_type)[2]()
        keybind = TT.all_tower_types.get(tower_type)[0]
    return tower_type, upgrades1, upgrades2, keybind


class Permutation:
    def __init__(self, grid, cancel_coord):
        """
        :param grid: The grid with all the possible pixel locations to place towers
        :param cancel_coord: The location to click on to cancel placing any tower
        """
        self.towers_wanted = []
        self.fitness = 0
        num_towers = random.randint(1, 3)
        for i in range(num_towers):
            tower_type, upgrades1, upgrades2, keybind = pick_tower()
            self.towers_wanted.append(Tower(tower_type, random.choice(random.choice(grid)), upgrades1, upgrades2, keybind, cancel_coord))

    def place_towers(self):
        for tower in self.towers_wanted:
            tower.place_tower()

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __repr__(self):
        return str(self.towers_wanted)