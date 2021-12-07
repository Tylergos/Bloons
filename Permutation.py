class Permutation:
    def __init__(self):
        self.towers_wanted = []
        num_towers = random.randint(1, 10)
        for i in range(num_towers):
            dictionary_num = random.randint(1, 3)
            if dictionary_num == 1:
                tower_index = random.randint(0, len(lead_towers))
                tower_type = list(lead_towers.keys())[tower_index]
                upgrades1 = lead_towers.get(tower_type)[1]()
                upgrades2 = lead_towers.get(tower_type)[2]()
                keybind = lead_towers.get(tower_type)[0]
            elif dictionary_num == 2:
                tower_index = random.randint(0, len(camo_towers))
                tower_type = list(camo_towers.keys())[tower_index]
                upgrades1 = camo_towers.get(tower_type)[1]()
                upgrades2 = camo_towers.get(tower_type)[2]()
                keybind = camo_towers.get(tower_type)[0]
            elif dictionary_num == 3:
                tower_index = random.randint(0, len(all_tower_types))
                tower_type = list(all_tower_types.keys())[tower_index]
                upgrades1 = all_tower_types.get(tower_type)[1]()
                upgrades2 = all_tower_types.get(tower_type)[2]()
                keybind = all_tower_types.get(tower_type)[0]
            # Need to fix the location stuff
            self.towers_wanted.append(tower_type, (0, 0), upgrades1, upgrades2, keybind)

    # Each parent maybe be an array of the towers placed (or at least wants to place)
    def crossover(parent1, parent2):
        # Not sure 100% what would be best for crossover, take a tower for each parent and swap them?
        index1 = random.randint(0, len(parent1))
        index2 = random.randint(0, len(parent2))
        temp1 = parent1[index1]
        temp2 = parent2[index2]
        parent1[index1] = temp2
        parent2[index2] = temp1
        return parent1, parent2