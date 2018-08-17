class Weapon:
    """CLass for all the objects in the game"""

    name = ''
    damage = 0
    crit_multiplier = 0.0
    stamina = 0
    wpn_range = 0

    def __init__(self, name):
        self.name = name

    def set_stats(self, damage, crit_multiplier, stamina, wpn_range):
        self.damage = damage
        self.crit_multiplier = crit_multiplier
        self.stamina = stamina
        self.wpn_range = wpn_range

    def get_damage(self):
        return self.damage

    def get_crit_multiplier(self):
        return self.crit_multiplier

    def get_stamina(self):
        return self.stamina

    def get_range(self):
        return self.wpn_range
