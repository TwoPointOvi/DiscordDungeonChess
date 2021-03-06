from Inventory import Inventory


class Player:
    """Class for the players that join the arena
        Information like health, armor and inventory will be saved"""
    health = 100
    armor = 0
    max_armor = 0
    stamina = 0
    max_stamina = 0
    luck = 1.0
    inventory = Inventory()
    position_x = 0
    position_y = 0

    def __init__(self, name, discord_id, author):
        self.name = name
        self.discord_id = discord_id
        self.author = author

    def set_position(self, x, y):
        self.position_x = x
        self.position_y = y

    def set_stats(self, health, armor, stamina):
        self.health = health
        self.armor = armor
        self.stamina = stamina

    def set_health(self, amount):
        self.health = amount

    def set_armor(self, amount):
        self.max_armor = amount

    def set_stamina(self, amount):
        self.stamina = amount

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

    def move(self, x, y):
        self.position_x += x
        self.position_y += y

    def attack(self, player, wpn_type):
        player.reduce_health(self.inventory.item_dic[wpn_type].damage)

