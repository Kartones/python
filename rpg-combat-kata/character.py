
class Character:

    CLASS_FIGHTER = "fighter"
    CLASS_RANGED = "ranged-fighter"

    CLASS_FIGHTER_ATTACK_DISTANCE = 2
    CLASS_RANGED_ATTACK_DISTANCE = 20

    def __init__(self, character_class, position):
        self.max_health = 1000
        self.current_health = self.max_health
        self.level = 1
        self.character_class = character_class
        self.position = position

    def health(self):
        return self.current_health

    def is_alive(self):
        return self.current_health > 0

    def is_dead(self):
        return not self.is_alive()

    def attack_range(self):
        if self.character_class == Character.CLASS_FIGHTER:
            return Character.CLASS_FIGHTER_ATTACK_DISTANCE
        elif self.character_class == Character.CLASS_RANGED:
            return Character.CLASS_RANGED_ATTACK_DISTANCE
        else:
            raise ValueError("Invalid character class {}".format(self.character_class))

    def receive_damage(self, amount):
        self.current_health = max([0, self.current_health - amount])

    def heal(self, amount):
        if not self.is_dead():
            self.current_health = min(self.max_health, self.current_health + amount)

    def move(self, position):
        self.position.move(position)
