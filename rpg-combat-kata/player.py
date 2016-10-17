
class Player:

    def __init__(self, character):
        self.character = character
        self.factions = []

    def heal(self, target, amount):
        if target == self or self.is_ally_of(target):
            target.character.heal(amount)

    def receive_damage(self, amount):
        self.character.receive_damage(amount)

    def attack(self, another_player, amount):
        if another_player != self and not self.is_ally_of(another_player) and self._are_in_range(self, another_player):
            another_player.receive_damage(self.actual_damage(another_player, amount))

    def actual_damage(self, another_player, amount):
        if self.character.level - another_player.character.level <= -5:
            return amount / 2
        elif self.character.level - another_player.character.level >= 5:
            return amount * 1.5
        else:
            return amount

    def move(self, position):
        self.character.position.move(position)

    def join_faction(self, faction):
        self.factions.append(faction)

    def leave_faction(self, faction):
        if faction in self.factions:
            self.factions.remove(faction)

    def is_ally_of(self, another_player):
        return len([faction for faction in self.factions if faction in another_player.factions]) > 0

    def _are_in_range(self, player, target):
        distance_between_players = \
            max(player.character.position.current_position(), target.character.position.current_position()) - \
            min(player.character.position.current_position(), target.character.position.current_position())
        return distance_between_players <= player.character.attack_range()
