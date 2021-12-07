import pyautogui as pag


class Tower:
    def __init__(self, tower_type, location, upgrades_path1, upgrades_path2, key_bind, cancel_coord):
        """
        :param tower_type: A string of the name of the tower
        :param location:  A tuple of the coordinates in pixels
        :param upgrades_path1: The number of upgrades in the first path
        :param upgrades_path2: The number of upgrades in the second path
        :param key_bind: The key bind of the tower type
        :param cancel_coord: The location to click on to cancel placing any tower
        """
        self.tower_type = tower_type
        self.location = location
        self.upgrades_path1 = upgrades_path1
        self.upgrades_path2 = upgrades_path2
        self.key_bind = key_bind
        self.cancel_coord = cancel_coord

    def __repr__(self):
        return self.tower_type


    def set_tower_type(self, new_tower_type):
        self.tower_type = new_tower_type

    def set_location(self, new_location):
        self.location = new_location

    def set_upgrades_path1(self, new_upgrades_path1):
        self.upgrades_path1 = new_upgrades_path1

    def set_upgrades_path2(self, new_upgrades_path2):
        self.upgrades_path2 = new_upgrades_path2

    def set_keybind(self, new_keybind):
        self.key_bind = new_keybind

    def place_tower(self):
        """
        Places and upgrades the tower in the coordinates of location attribute
        """
        pag.press(self.key_bind)
        pag.click(self.location[0], self.location[1])
        # currently favours first upgrade path if both are more than 2
        for _ in range(self.upgrades_path1):
            pag.press(',')
        for _ in range(self.upgrades_path2):
            pag.press('.')
        # click at cancel coord to prevent any possible errors
        pag.click(self.cancel_coord[0], self.cancel_coord[1])