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

        # Towers can only go 3 or 4 upgrades on one path at a time, that's why some have 2 different options
        lead_towers = {"Dart Monkey": ["q", lambda: 4, lambda: random.randint(0, 2)],
                       "Boomerang Monkey": ["r", lambda: random.randint(0, 2), lambda: random.randint(2, 4)],
                       "Bomb Shooter 1": ["y", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                       "Bomb Shooter 2": ["y", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                       "Tack Shooter": ["w", lambda: 4, lambda: random.randint(0, 2)],
                       "Ice Monkey 1": ["a", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                       "Ice Monkey 2": ["a", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                       "Glue Monkey 1": ["s", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                       "Glue Monkey 2": ["s", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                       "Sniper Monkey 1": ["e", lambda: random.randint(1, 4), lambda: random.randint(0, 2)],
                       "Sniper Monkey 2": ["e", lambda: random.randint(1, 2), lambda: random.randint(0, 4)],
                       "Wizard Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                       "Wizard Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                       "Super Monkey": ["g", lambda: 2, lambda: random.randint(0, 4)],
                       "Bloonchipper": [";", lambda: 2, lambda: random.randint(0, 4)]}

        camo_towers = {"Dart Monkey": ["q", lambda: 2, lambda: random.randint(0, 4)],
                       "Boomerang Monkey": ["r", lambda: 4, lambda: random.randint(0, 2)],
                       "Sniper Monkey": ["e", lambda: random.randint(0, 4), lambda: 2],
                       "Wizard Monkey": ["h", lambda: random.randint(0, 4), lambda: 2],
                       "Ninja Monkey 1": ["t", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                       "Ninja Monkey 2": ["t", lambda: random.randint(0, 2), lambda: random.randint(0, 4)]}

        all_tower_types = {"Dart Monkey 1": ["q", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Dart Monkey 2": ["q", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Boomerang Monkey 1": ["r", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Boomerang Monkey 2": ["r", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Bomb Shooter 1": ["y", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Bomb Shooter 2": ["y", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Tack Shooter 1": ["w", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Tack Shooter 2": ["w", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Ice Monkey 1": ["a", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Ice Monkey 2": ["a", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Glue Monkey 1": ["s", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Glue Monkey 2": ["s", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Sniper Monkey 1": ["e", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Sniper Monkey 2": ["e", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Ninja Monkey 1": ["t", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Ninja Monkey 2": ["t", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Super Monkey 1": ["g", lambda: random.randint(0, 3), lambda: random.randint(0, 2)],
                           "Super Monkey 2": ["g", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Bloonchipper  1": [";", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Bloonchipper 2": [";", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           "Wizard Monkey 1": ["h", lambda: random.randint(0, 4), lambda: random.randint(0, 2)],
                           "Wizard Monkey 2": ["h", lambda: random.randint(0, 2), lambda: random.randint(0, 4)],
                           }