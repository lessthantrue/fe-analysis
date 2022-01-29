import pandas as pd
import numpy as np

stats = [ 'hp', 'str', 'skl', 'spd', 'lck', 'def', 'res' ]
weapons = [ 'sword', 'lance', 'axe', 'anima', 'dark', 'light', 'staff', 'bow']

def put_dict_items_in_lists(dict):
    return { k : [v] for k, v in dict.items() }

class PlayerUnit():
    def __init__(self):
        pass

    def from_yaml(dict):
        toReturn = PlayerUnit()
        toReturn.fill_from_yaml(dict)
        return toReturn

    def fill_from_yaml(self, dict):
        self.stats = pd.DataFrame.from_dict(put_dict_items_in_lists(dict['bases']))[stats]
        self.level = dict['bases']['lvl']
        self.growths = pd.DataFrame.from_dict(put_dict_items_in_lists(dict['growths'])) / 100
        self.weapon_rank = { w : None for w in weapons }
        self.weapon_rank.update(dict['weapons'])
        self.unit_class = dict['class']
        self.promoted = dict['promoted']

    def stdev_of_stats(self, level):
        # not sure if this works
        up_levels = level - self.level
        return np.sqrt(up_levels * self.growths * (1 - self.growths))

    def stats_leveled_to(self, level):
        up_levels = level - self.level
        return self.stats + self.growths * up_levels

if __name__ == "__main__":
    import yaml
    with open("fe6_units.yaml", "r") as y:
        unit_yaml = yaml.load(y)
        roy = PlayerUnit.from_yaml(unit_yaml['Marcus'])
        print(roy.stats_leveled_to(10))
        print(roy.stdev_of_stats(10))