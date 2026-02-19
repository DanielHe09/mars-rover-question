"""
Mars Rover tests – implement the solution so these pass.
"""
import pytest

from rover import Rover
from plateau import Plateau
from position import Position
from instructions import Instruction, Instructions
from exceptions import (
    PositionNotOnPlateauException,
    NotDroppedException,
    UnknownInstructionException,
)


def instructions_from_string(s):
    """Convert string like 'LMLMLMLMM' to list of Instruction."""
    return Instructions(s).get_instructions()


class TestRoverRide:
    @pytest.fixture
    def plateau(self):
        return Plateau(5, 5)

    def test_moving_rover_one_should_succeed(self, plateau):
        rover = Rover("Opportunity")
        rover.drop_rover(plateau, 1, 2, "N")
        rover.process_instructions(instructions_from_string("LMLMLMLMM"))
        assert rover.report_position() == "1 3 N"

    def test_moving_rover_two_should_succeed(self, plateau):
        rover = Rover("Opportunity")
        rover.drop_rover(plateau, 3, 3, "E")
        rover.process_instructions(instructions_from_string("MMRMMRMRRM"))
        assert rover.report_position() == "5 1 E"

    def test_moving_rover_beyond_plateau_should_throw(self, plateau):
        rover = Rover("Opportunity")
        rover.drop_rover(plateau, 2, 2, "N")
        with pytest.raises(PositionNotOnPlateauException) as exc_info:
            rover.process_instructions(instructions_from_string("MMMMMMMM"))
        assert exc_info.value.args[0] == "Position is not on the plateau!"

    def test_dropping_rover_beyond_plateau_should_throw(self, plateau):
        rover = Rover("Opportunity")
        with pytest.raises(PositionNotOnPlateauException) as exc_info:
            rover.drop_rover(plateau, 6, 6, "N")
        assert exc_info.value.args[0] == "Position is not on the plateau!"

    def test_not_dropped_rover_should_report_properly(self):
        rover = Rover("Opportunity")
        assert rover.report_position() == "Not dropped yet."

    def test_moving_an_undropped_rover_should_throw(self, plateau):
        rover = Rover("Opportunity")
        with pytest.raises(NotDroppedException) as exc_info:
            rover.process_instructions(instructions_from_string("MMMMMM"))
        assert exc_info.value.args[0] == "Rover was not dropped on the plateau!"

    def test_unknown_instruction_should_throw(self, plateau):
        rover = Rover("Opportunity")
        with pytest.raises(UnknownInstructionException):
            rover.process_instructions(instructions_from_string("XXXX"))

    def test_moving_rover_over_another_rover_should_throw(self, plateau):
        one = Rover("Curiosity")
        two = Rover("Opportunity")
        one.drop_rover(plateau, "3 5 E")
        with pytest.raises(RuntimeError):
            two.drop_rover(plateau, "3 5 N")

    def test_dropping_at_10_10_should_give_exact_report(self):
        plat = Plateau(20, 20)
        one = Rover("Curiosity")
        one.drop_rover(plat, "10 10 N")
        assert one.report_position() == "10 10 N"

    def test_dropping_two_rovers_next_to_another_should_succeed(self, plateau):
        one = Rover("Curiosity")
        two = Rover("Opportunity")
        one.drop_rover(plateau, "3 5 E")
        two.drop_rover(plateau, "4 5 N")
