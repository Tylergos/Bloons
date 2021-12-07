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