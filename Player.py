class Player:
    """Class for the players that join the arena
        Information like health, armor and inventory will be saved"""
    health = 100
    armor = 0
    stamina = 0
    luck = 1.0

    def __init__(self, name, discord_id):
        self.name = name
        self.discord_id = discord_id

    def set_stats(self, health, armor, stamina):
        self.health = health
        self.armor = armor
        self.stamina = stamina

    def reduce_health(self, amount):
        self.health -= amount

    def reduce_armor(self, amount):
        self.armor -= amount

    def reduce_stamina(self, amount):
        self.stamina -= amount

    def increase_health(self, amount):
        self.health -= amount

    def increase_armor(self, amount):
        self.armor -= amount

    def increase_stamina(self, amount):
        self.stamina -= amount

    def set_luck(self, luck):
        self.luck = luck

    def reset_luck(self):
        self.luck = 1.0
