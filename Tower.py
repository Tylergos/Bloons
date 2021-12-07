class Tower:
    def __init__(self, tower_type, location, upgrades_path1, upgrades_path2, key_bind):
        self.tower_type = tower_type
        self.location = location
        self.upgrades_path1 = upgrades_path1
        self.upgrades_path2 = upgrades_path2
        self.key_bind = key_bind


    def set_tower_type(self, new_tower_type):
        self.tower_type = new_tower_type


    def set_location(self, new_location):
        self.location = new_location


    def set_upgrades_path1(self, new_upgrades_path1):
        self.upgrades_path1 = new_upgrades_path1


    def set_upgrades_path2(self, new_upgrades_path2):
        self.upgrades_path2 = new_upgrades_path2


    def place_tower(self):
        pag.press(self.key_bind)
        pag.click(self.location[0], self.location[1])
        for _ in range(self.upgrades_path1):
            pag.press(',')
        for _ in range(self.upgrades_path2):
            pag.press('.')
