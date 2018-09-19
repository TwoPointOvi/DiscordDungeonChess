class Inventory:
    """Class for the inventory of the players where objects are stored"""

    item_list = []
    item_dic = {
        'melee': '',
        'long_range': '',
        'consumable1': '',
        'consumable2': '',
        'armor': ''}

    def __init__(self):
        self.item_list = []

    def add_item(self, new_item):
        self.item_list.append(new_item)

    def add_item(self, new_item, slot):
        self.item_list[slot] = new_item

    def replace_item(self, new_item, slot):
        self.item_list[slot] = new_item

    def remove_item(self, slot):
        del self.item_listp[slot]

