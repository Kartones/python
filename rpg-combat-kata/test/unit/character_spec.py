# PYTHONPATH=.test/ mamba test/unit

from doublex import *
from expects import *
from doublex_expects import *

from character import *

MAX_CHARACTER_HEALTH = 1000


with description("Character"):

    with before.each:
        self.character = Character(character_class=Character.CLASS_FIGHTER, position=Stub())

    with context("character attributes"):
        with it("has a starting health"):
            expect(self.character.health()).to(equal(MAX_CHARACTER_HEALTH))

        with it("has a starting level"):
            expect(self.character.level).to(equal(1))

        with it("has a starting position"):
            with Spy() as position:
                position.current_position().returns(0)
            character = Character(character_class=Character.CLASS_FIGHTER, position=position)
            expect(character.position.current_position()).to(equal(0))

    with context("character status"):
        with it("starts alive"):
            expect(self.character.is_alive()).to(be_true)
            expect(self.character.is_dead()).to(be_false)

        with it("has a defined range if is fighter class"):
            expect(self.character.attack_range()).to(equal(Character.CLASS_FIGHTER_ATTACK_DISTANCE))

        with it("has a defined range if is ranged class"):
            character = Character(character_class=Character.CLASS_RANGED, position=Stub())
            expect(character.attack_range()).to(equal(Character.CLASS_RANGED_ATTACK_DISTANCE))

    with context("receiving damage"):
        with it("can be dead if damaged enough"):
            self.character.receive_damage(MAX_CHARACTER_HEALTH)
            expect(self.character.is_alive()).to(be_false)
            expect(self.character.is_dead()).to(be_true)

        with it("doesn't dies if receives small enough damage"):
            self.character.receive_damage(500)
            expect(self.character.is_alive()).to(be_true)
            self.character.receive_damage(100)
            expect(self.character.is_alive()).to(be_true)

        with it("health stays at 0 even if receives huge damage"):
            self.character.receive_damage(5000)
            expect(self.character.health()).to(equal(0))

    with context("healing"):
        with it("can be healed if alive"):
            self.character.receive_damage(500)
            self.character.heal(100)
            expect(self.character.health()).to(equal(600))

        with it("cannot be healed over maximum health"):
            self.character.heal(500)
            expect(self.character.health()).to(equal(MAX_CHARACTER_HEALTH))

            self.character.receive_damage(100)
            self.character.heal(500)
            expect(self.character.health()).to(equal(MAX_CHARACTER_HEALTH))

        with it("cannot be healed if dead"):
            self.character.receive_damage(5000)
            self.character.heal(100)
            expect(self.character.is_alive()).to(be_false)

    with context("movement"):
        with it("can move to another position"):
            position = Spy()
            character = Character(character_class=Character.CLASS_FIGHTER, position=position)
            character.move(10)
            expect(character.position.move).to(have_been_called_with(10))
