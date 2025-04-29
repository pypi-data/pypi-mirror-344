from __future__ import annotations

from cohdl import (
    Bit,
    BitVector,
    Unsigned,
    Signed,
    Port,
    Signal,
    Entity,
    pyeval,
    Null,
    Full,
)
from cohdl import std

import cohdl
import sys
from dataclasses import dataclass


GRID_SIZE = 9
BLOCK_SIZE = 3
CELL_CNT = 81


@dataclass
class CellUpdate:
    new_cell: Cell
    new_solution: bool
    valid_solutions: BitVector
    valid_cnt: Unsigned


class Cell(std.Record):
    options: BitVector[GRID_SIZE]

    def __bool__(self):
        return bool(self.options)

    def gen_next(self, invalid_mask: BitVector[GRID_SIZE]):
        valid_mask = ~invalid_mask

        found_solution = False if self.options else std.is_one_hot(valid_mask)

        return (
            Cell(options=valid_mask if found_solution else self.options),
            found_solution,
            valid_mask,
            std.count_set_bits(
                valid_mask
                if not (found_solution or self.options)
                else std.ones(GRID_SIZE)
            ),
        )


op_or = lambda a, b: a | b

import itertools


class CheckDuplicates(cohdl.Entity):
    result = Port.output(Bit)

    @classmethod
    @pyeval
    def connection_dict(self, inp):
        assert len(inp) == GRID_SIZE

        return {f"inp_{nr}": elem for nr, elem in enumerate(inp)}

    def architecture(self):

        inp = []

        for nr in range(GRID_SIZE):
            p = Port.input(BitVector[GRID_SIZE], name=f"inp_{nr}")
            std.add_entity_port(type(self), p)
            inp.append(p)

        @std.concurrent
        def logic():
            collision_masks = []
            ored = []

            def add_collision(inp):
                std.as_pyeval(
                    list.append,
                    collision_masks,
                    std.binary_fold(
                        op_or,
                        [
                            a & b
                            for a, b in std.as_pyeval(itertools.product, inp, inp)
                            if a is not b
                        ],
                    ),
                )

            for a in range(0, GRID_SIZE, BLOCK_SIZE):
                val = inp[a : a + BLOCK_SIZE]
                add_collision(val)
                std.as_pyeval(list.append, ored, std.binary_fold(op_or, val))

            add_collision(ored)

            self.result <<= any(collision_masks)

        return super().architecture()


def contains_duplicates(inp: list[BitVector[GRID_SIZE]]):
    assert len(inp) == GRID_SIZE

    return std.OpenEntity[CheckDuplicates](
        **CheckDuplicates.connection_dict(inp)
    ).result


class Sudoku(std.Record):
    cells: std.Array[Cell, CELL_CNT]

    def is_done(self):
        return all(self.cells)

    @pyeval
    def _block_indicies(self, nr):
        block_x = (nr % BLOCK_SIZE) * BLOCK_SIZE
        block_y = (nr // BLOCK_SIZE) * BLOCK_SIZE

        indices = []

        for r in range(BLOCK_SIZE):
            for c in range(BLOCK_SIZE):
                col = block_x + c
                row = block_y + r

                indices.append(row * GRID_SIZE + col)

        return indices

    def get_row(self, nr):
        return [self.cells[GRID_SIZE * nr + idx].options for idx in range(GRID_SIZE)]

    def get_column(self, nr):
        return [self.cells[nr + GRID_SIZE * idx].options for idx in range(GRID_SIZE)]

    def get_block(self, nr):
        return [self.cells[idx].options for idx in self._block_indicies(nr)]

    def gen_next(self):

        bf = std.binary_fold

        row_masks = [bf(op_or, self.get_row(nr)) for nr in range(GRID_SIZE)]
        col_masks = [bf(op_or, self.get_column(nr)) for nr in range(GRID_SIZE)]
        blk_masks = [bf(op_or, self.get_block(nr)) for nr in range(GRID_SIZE)]

        row_invalid = [contains_duplicates(self.get_row(nr)) for nr in range(GRID_SIZE)]
        col_invalid = [
            contains_duplicates(self.get_column(nr)) for nr in range(GRID_SIZE)
        ]
        blk_invalid = [
            contains_duplicates(self.get_block(nr)) for nr in range(GRID_SIZE)
        ]

        any_invalid = any(row_invalid) or any(col_invalid) or any(blk_invalid)

        def update_cell(idx: int):
            row = idx // GRID_SIZE
            col = idx % GRID_SIZE
            blk = (row // BLOCK_SIZE) * BLOCK_SIZE + (col // BLOCK_SIZE)

            return self.cells[idx].gen_next(
                row_masks[row] | col_masks[col] | blk_masks[blk]
            )

        update_result = [update_cell(idx) for idx in range(CELL_CNT)]

        cell_updates = [elem[0] for elem in update_result]
        cell_changed = [elem[1] for elem in update_result]
        cell_valid = [elem[2] for elem in update_result]

        return (
            any_invalid,
            any(cell_changed),
            Sudoku(cells=cell_updates),
            cell_valid,
            std.min_index([elem[3] for elem in update_result]),
        )


class SudokuPos(Sudoku):
    guess: BitVector[GRID_SIZE]


class SudokuSolver(Entity):
    clk = Port.input(Bit)

    start = Port.input(Bit)
    data_inp = Port.input(BitVector[GRID_SIZE * CELL_CNT])
    data_out = Port.output(BitVector[GRID_SIZE * CELL_CNT])

    done = Port.output(Bit, default=False)
    valid = Port.output(Bit, default=False)

    dbg_a = Port.output(Unsigned[3], default=Null)
    dbg_size = Port.output(Unsigned[8], default=Null)
    dbg_solved_cnt = Port.output(Unsigned[8], default=Null)

    def architecture(self):
        ctx = std.SequentialContext(std.Clock(self.clk))

        current_sudoku = std.Signal[SudokuPos]()
        next_sudoku = std.Signal[Sudoku]()
        invalid = Signal[Bit]()
        changes = Signal[Bit]()
        next_guess = Signal[BitVector[GRID_SIZE]](Null)
        next_idx = Signal[Unsigned.upto(CELL_CNT)](Null)

        @std.concurrent
        def logic_update():
            nonlocal next_sudoku, invalid, changes, next_guess, next_idx

            update_result = current_sudoku.gen_next()

            invalid <<= update_result[0]
            changes <<= update_result[1]
            next_sudoku <<= update_result[2]
            next_idx <<= update_result[4]

            cells_valid = std.concat(*update_result[3][::-1])
            cell_valid = std.select_batch(
                cells_valid, std.one_hot(CELL_CNT, next_idx), GRID_SIZE
            )

            next_guess <<= std.choose_first(
                *[
                    (
                        cell_valid & (current_sudoku.guess.unsigned << nr).bitvector,
                        (current_sudoku.guess.unsigned << nr),
                    )
                    for nr in range(GRID_SIZE)
                ],
                default=Null,
            )

            self.data_out <<= std.to_bits(current_sudoku.cells)

            self.dbg_solved_cnt <<= std.count(
                current_sudoku.cells, check=lambda x: bool(x.options)
            )

        @ctx
        async def proc_solve():
            nonlocal current_sudoku, next_sudoku, invalid
            self.dbg_a <<= 0
            self.dbg_size <<= 0
            await self.start
            self.dbg_a <<= 1

            inp_sudoku = std.from_bits[Sudoku](self.data_inp)

            current_sudoku.cells <<= inp_sudoku.cells
            current_sudoku.guess <<= std.one_hot(GRID_SIZE, 0)

            stack = std.Stack[SudokuPos, CELL_CNT]()

            is_done = cohdl.always(current_sudoku.is_done())

            while True:
                self.dbg_size <<= stack.size()
                if invalid or (not is_done and not changes and next_guess == Null):
                    self.dbg_a <<= 2
                    if stack.empty():
                        self.done ^= True
                        self.valid ^= False
                        break
                    else:
                        temp_guess = stack.pop()
                        current_sudoku <<= temp_guess

                elif is_done:
                    self.dbg_a <<= 3
                    self.done ^= True
                    self.valid ^= True
                    break

                elif changes:
                    self.dbg_a <<= 4

                    current_sudoku.cells <<= next_sudoku.cells

                else:
                    self.dbg_a <<= 5

                    stack.push(
                        SudokuPos(
                            current_sudoku.cells,
                            next_guess.unsigned << 1,
                        )
                    )

                    current_sudoku.cells[next_idx].options <<= next_guess
                    current_sudoku.guess <<= std.one_hot(GRID_SIZE, 0)


#
#
#
#
#
#
#
#
#
# cohdl.use_pretty_traceback(False)
# std.VhdlCompiler.to_string(SudokuSolver)
# exit()

from cohdl_sim import Simulator


sim = Simulator(
    SudokuSolver,
    sim_args=["--vcd=waveform.vcd"],
    # no_build_update=True,
    # additional_vhdl=["build/vhdl/SudokuSolver.vhd"],
)


@sim.test
async def test_bench(dut: SudokuSolver):
    with open("sudoku.log", "w") as file:

        def log(*args, **kwargs):
            print(*args, **kwargs)

        sim.gen_clock(dut.clk, std.GHz(1))

        def set_digit(cell, val):
            off = cell * GRID_SIZE

            dut.data_inp[off + GRID_SIZE - 1 : off] <<= (
                std.one_hot(GRID_SIZE, val - 1) if val != 0 else Null
            )

        def set_all(content):
            for cell_nr, val in enumerate(content):
                set_digit(cell_nr, val)

        def get_digit(row, col, from_inp=False):
            cell = (col * GRID_SIZE) + row * CELL_CNT

            vec = dut.data_inp if from_inp else dut.data_out

            val = vec[cell + GRID_SIZE - 1 : cell].copy()

            if val == Null:
                return 0

            for nr in range(GRID_SIZE):
                if val == std.one_hot(GRID_SIZE, nr):
                    return nr + 1

            return "."

        def show(from_inp=False):
            for row in range(GRID_SIZE):
                log(
                    *[
                        get_digit(row, col, from_inp=from_inp)
                        for col in range(GRID_SIZE)
                    ]
                )
            log()

        #
        #
        #

        # file_path = "/home/alexander/dev/tmp/tdoku/data/puzzles7_serg_benchmark"

        file_path = "/home/alexander/dev/tmp/tdoku/data/puzzles5_forum_hardest_1905_11+"

        with open(file_path) as file:
            nr = 0
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue

                if nr > 5:
                    break

                nr += 1
                assert len(line) == 81, f"invalid line length: '{line}'"

                print(f"nr ------- {nr}")

                for row in range(9):
                    print(line[row * 9 : row * 9 + 9])

                line = line.replace(".", "0")
                content = [int(c) for c in line]

                dut.start <<= True
                set_all(content)

                for _ in range(10000):
                    await sim.rising_edge(dut.clk)

                    if _ > 2:
                        dut.start <<= False

                    # print(" IIIII ")
                    # show(from_inp=True)

                    print(" XXXXX ", dut.dbg_size, dut.dbg_solved_cnt, dut.dbg_a)
                    # show()
                    # print()

                    if dut.done:
                        show()
                        print()
                        return
                else:
                    print("Solver failed")
                    print()

                    show()

                    return
