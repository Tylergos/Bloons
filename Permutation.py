from Tower import Tower
import random
import TowerTypes as TT


class Permutation:
    def __init__(self, cancel_coord):
        """
        :param cancel_coord: The location to click on to cancel placing any tower
        """
        self.towers_wanted = []
        num_towers = random.randint(1, 10)
        for i in range(num_towers):
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
            # Need to fix the location stuff
            self.towers_wanted.append(Tower(tower_type, (0, 0), upgrades1, upgrades2, keybind, cancel_coord))
    def __repr__(self):
        return str(self.towers_wanted)
