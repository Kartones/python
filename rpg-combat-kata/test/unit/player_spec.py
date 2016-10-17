from doublex import *
from expects import *
from doublex_expects import *

from player import *
# for constants only
from character import *


with description("Player"):

    with before.each:
        with Stub() as self.position:
            self.position.current_position().returns(0)
        with Stub() as self.character:
            self.character.level = 1
            self.character.position = self.position
            self.character.attack_range().returns(2)
        self.player = Player(character=self.character)

    with context("starting elements"):
        with it("has a starting character"):
            expect(self.player.character).not_to(equal(None))

        with it("has no starting factions"):
            expect(self.player.factions).to(equal([]))

    with context("actions"):
        with it("can heal himself"):
            character = Spy()
            player = Player(character=character)
            player.heal(target=player, amount=100)
            expect(character.heal).to(have_been_called_with(100))

        with it("can receive damage"):
            character = Spy()
            player = Player(character=character)
            player.receive_damage(100)
            expect(character.receive_damage).to(have_been_called_with(100))

        with it("can damage other player"):
            with Stub() as another_player_position:
                another_player_position.current_position().returns(0)
            with Spy() as another_player_character:
                another_player_character.level = 1
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)
            self.player.attack(another_player, 200)
            expect(another_player_character.receive_damage).to(have_been_called_with(200))

        with it("can join factions"):
            self.player.join_faction("a_faction")
            expect(self.player.factions).to(equal(["a_faction"]))
            self.player.join_faction("another_faction")
            expect(self.player.factions).to(equal(["a_faction", "another_faction"]))

        with it("can leave factions"):
            self.player.join_faction("a_faction")
            self.player.join_faction("another_faction")
            self.player.leave_faction("a_faction")
            expect(self.player.factions).to(equal(["another_faction"]))

        with it("can move to another position"):
            position = Spy()
            with Stub() as character:
                character.position = position
            player = Player(character=character)
            player.move(5)
            expect(position.move).to(have_been_called_with(5))

    with context("alliances"):
        with it("is not ally of a player without faction"):
            self.player.join_faction("a_faction")
            another_player = Player(character=Stub())
            expect(self.player.is_ally_of(another_player)).to(be_false)

        with it("is ally with a player of same faction"):
            self.player.join_faction("a_faction")
            another_player = Player(character=Stub())
            another_player.join_faction("a_faction")
            expect(self.player.is_ally_of(another_player)).to(be_true)

        with it("is not ally with a player of different faction"):
            self.player.join_faction("a_faction")
            another_player = Player(character=Stub())
            another_player.join_faction("another_faction")
            expect(self.player.is_ally_of(another_player)).to(be_false)

    with context("healing restrictions"):
        with it("can heal an ally"):
            self.player.join_faction("a_faction")
            another_player_character = Spy()
            another_player = Player(character=another_player_character)
            another_player.join_faction("a_faction")
            self.player.heal(target=another_player, amount=100)
            expect(another_player_character.heal).to(have_been_called_with(100))

        with it("cannot heal a non-ally"):
            self.player.join_faction("a_faction")
            another_player_character = Spy()
            another_player = Player(character=another_player_character)
            another_player.join_faction("another_faction")
            self.player.heal(target=another_player, amount=100)
            expect(another_player_character.heal).not_to(have_been_called)

    with context("damage restrictions and modifiers"):
        with it("cannot damage himself"):
            character = Spy()
            player = Player(character=character)
            player.attack(player, 100)
            expect(character.receive_damage).not_to(have_been_called)

        with it("If the target is 5 or more levels above the player, the damage applied will be reduced by 50%"):
            with Stub() as another_player_position:
                another_player_position.current_position().returns(0)
            with Spy() as another_player_character:
                another_player_character.level = 6
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)
            self.player.attack(another_player, 100)
            expect(another_player_character.receive_damage).to(have_been_called_with(50))

        with it("If the target is 5 or more levels below the player, the damage applied will be boosted by 50%"):
            with Stub() as position:
                position.current_position().returns(0)
            with Stub() as character:
                character.level = 6
                character.position = position
                character.attack_range().returns(2)
            player = Player(character=character)

            with Stub() as another_player_position:
                another_player_position.current_position().returns(0)
            with Spy() as another_player_character:
                another_player_character.level = 1
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)
            player.attack(another_player, 100)
            expect(another_player_character.receive_damage).to(have_been_called_with(150))

        with it("doesn't does damage if target is not in range"):
            with Stub() as position:
                position.current_position().returns(0)
            with Stub() as character:
                character.level = 1
                character.position = position
                character.attack_range().returns(2)
            player = Player(character=character)

            with Stub() as another_player_position:
                another_player_position.current_position().returns(5)
            with Spy() as another_player_character:
                another_player_character.level = 1
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)

            player.attack(another_player, 100)
            expect(another_player_character.receive_damage).not_to(have_been_called)

        with it("doesn't does damage to faction allies"):
            self.player.join_faction("a_faction")
            with Stub() as another_player_position:
                another_player_position.current_position().returns(0)
            with Spy() as another_player_character:
                another_player_character.level = 1
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)
            another_player.join_faction("a_faction")
            self.player.attack(another_player, 200)
            expect(another_player_character.receive_damage).not_to(have_been_called)

        with it("does does damage to other faction players"):
            self.player.join_faction("a_faction")
            with Stub() as another_player_position:
                another_player_position.current_position().returns(0)
            with Spy() as another_player_character:
                another_player_character.level = 1
                another_player_character.position = another_player_position
            another_player = Player(character=another_player_character)
            another_player.join_faction("another_faction")
            self.player.attack(another_player, 200)
            expect(another_player_character.receive_damage).to(have_been_called_with(200))
