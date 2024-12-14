class Character:
    def __init__(self, name, hp, mp, attack):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.inventory = []

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)

    def recover_health(self, amount):
        self.hp += amount

    def use_item(self, item):
        if item in self.inventory:
            if item['type'] == 'healing':
                self.recover_health(item['effect'])
            self.inventory.remove(item)