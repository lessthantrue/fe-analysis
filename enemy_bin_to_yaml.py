import sys
import struct
from collections import namedtuple
import yaml

f_bin = sys.argv[1]

EnemyData = namedtuple('EnemyData',
    [
        "type",
        "level",
        "x",
        "y",
        "hp",
        "strength",
        "skill",
        "speed",
        "defense",
        "resistance",
        "luck",
        "item1",
        "item2",
        "item3",
        "item4",
        "item5"
    ])

len_data_packed = 72
unpack_format = ("x"*12) + "HxxBxxxxxBBBxBBBBBBxxxxBxBxBxBxBxxx" + ("x" * 24)

# read class map yaml
with open("fe6_class_map.yaml") as y:
    class_yaml = yaml.safe_load(y)
    class_dict = { int(k, 16) : v for k, v in class_yaml.items() }

# read item map yaml
with open("fe6_item_map.yaml") as y:
    item_yaml = yaml.safe_load(y)
    item_dict = { int(k, 16) : v for k, v in item_yaml.items() }

def edata_item_list(edata):
    return [edata.item1, edata.item2, edata.item3, edata.item4, edata.item5]

def validate_enemy_data(edata):
    validations = [
        # (f"Level {edata.level} not in bounds", edata.level > 0 and edata.level <= 40),
        (f"Class {edata.type} not in map", edata.type in class_dict),
        (f"One of these items {edata_item_list(edata)} not in map", all([ i in item_dict for i in edata_item_list(edata)]))
    ]
    for msg, check in validations:
        if not check:
            # print(msg)
            return False
    return True

def edata_to_yaml_dict(edata : EnemyData):
    return {
        'stats': {
            'lvl': edata.level,
            'hp' : edata.hp,
            'str': edata.strength,
            'skl': edata.skill,
            'spd': edata.speed,
            'lck': edata.luck,
            'def': edata.defense,
            'res': edata.resistance,
        },
        'class': edata.type,
        'inventory': edata_item_list(edata)
    }

def create_enemy_data(data):
    toReturn = EnemyData._make(struct.unpack(unpack_format, data))
    if not validate_enemy_data(toReturn):
        return None
    toReturn = toReturn._replace(item1=item_dict[toReturn.item1])
    toReturn = toReturn._replace(item2=item_dict[toReturn.item2])
    toReturn = toReturn._replace(item3=item_dict[toReturn.item3])
    toReturn = toReturn._replace(item4=item_dict[toReturn.item4])
    toReturn = toReturn._replace(item5=item_dict[toReturn.item5])
    toReturn = toReturn._replace(type=class_dict[toReturn.type])
    return toReturn

enemies = []
with open(f_bin, mode='rb') as bin:
    data = bin.read()
    # for i in range(len(data) // len_data_packed):
    for i in range(len(data) // len_data_packed):
        start = i * len_data_packed
        end = start + len_data_packed
        enemy = create_enemy_data(data[start:end])
        if enemy != None:
            enemies.append(enemy)

base_bin_name = f_bin.split(".")[0]
with open(base_bin_name + ".yaml", 'w') as f:
    enemies_as_yaml = [ edata_to_yaml_dict(e) for e in enemies ]
    yaml.safe_dump(enemies_as_yaml, f, default_flow_style=None)
