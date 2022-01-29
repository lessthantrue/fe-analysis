classes_promoted = [
    "Hero",
    "Sword Master",
    "Warrior",
    "General",
    "Sniper",
    "Bishop",
    "Sage",
    "Druid",
    "Paladin",
    "Valkyrie",
    "Nomadic Trooper",
    "Falcoknight",
    "Dragon Master",
    "Berserker"
]

classes_bonus_40 = ["Bishop", "Valkyrie"]

class FE6Calculations():
    def __init__():
        pass

    # triangle can be 1 (good vs defender), -1 (bad vs defender), or 0 (same) 
    def damage(self, strength, weapon, defense, triangle=0, effective=False):
        effective_multiplier = 3 if effective else 1
        return strength + (weapon + triangle) * effective_multiplier

    def atk_speed(self, speed, weight, con):
        return speed - max(0, weight - con)

    def doubles(self, atk_unit, atk_other):
        return atk_unit - atk_other >= 4

    def damage_exp(self, unit_class, unit_level, other_class, other_level):
        other_class_bonus_a = 20 if other_class in classes_promoted else 0
        unit_class_bonus_a = 20 if unit_class in classes_promoted else 0
        return (
            31 + (other_level + other_class_bonus_a) - 
            (unit_level + unit_class_bonus_a)) / self.class_power(unit_class)

    def class_power(self, unit_class):
        if unit_class in ["Soldier", "Troubador", "Bard", "Priest", "Thief"]:
            return 2
        elif unit_class == "Paladin":
            return 4
        elif unit_class in ["Dark Dragon", "Makute", "King"]:
            return 5
        else:
            return 3