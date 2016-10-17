from doublex import *
from expects import *
from doublex_expects import *

from position import *


with description("Position"):
    with before.each:
        self.position = Position()

    with context("features"):
        with it("has an initial position"):
            expect(self.position.current_position()).to(equal(0))

        with it("position can change"):
            self.position.move(5)
            expect(self.position.current_position()).to(equal(5))
