from __future__ import annotations

from cohdl import (
    Bit,
    BitVector,
    Unsigned,
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

sys.setrecursionlimit(10000)

cohdl.pyeval

# cohdl.use_pretty_traceback(False)

GRID_SIZE = 9
BLOCK_SIZE = 3
CELL_CNT = 81

if False:
    GRID_SIZE = 4
    BLOCK_SIZE = 2
    CELL_CNT = 16


@pyeval
def bit_map(w: int, final_w):
    T = Unsigned.upto(final_w)
    return {nr: T(nr.bit_count()) for nr in range(2**w)}


def cnt_bits(inp: BitVector):
    batches = std.batched(inp, 5, allow_partial=True)
    fallback = Unsigned.upto(9)(Full)

    return std.batched_fold(
        lambda a, b: a + b,
        [
            std.select(batch.unsigned, bit_map(len(batch), 9), default=fallback)
            for batch in batches
        ],
    )


def min_pair(a, b):
    return a if a[0] < b[0] else b


@dataclass
class CellUpdate:
    new_state: BitVector
    new_solution: bool
    valid_solutions: BitVector
    valid_cnt: Unsigned

    @staticmethod
    def new(state: BitVector[GRID_SIZE], invalid_mask: BitVector[GRID_SIZE]):
        valid_mask = ~invalid_mask

        found_solution = False if state else std.is_one_hot(valid_mask)

        return CellUpdate(
            new_state=valid_mask if found_solution else state,
            new_solution=found_solution,
            valid_solutions=valid_mask,
            valid_cnt=cnt_bits(
                valid_mask if not (found_solution or state) else std.ones(GRID_SIZE)
            ),
        )


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
            cnt_bits(
                valid_mask
                if not (found_solution or self.options)
                else std.ones(GRID_SIZE)
            ),
        )


op_or = lambda a, b: a | b

import itertools


def contains_duplicates(inp: list[BitVector[GRID_SIZE]]):
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
        std.as_pyeval(ored.append, std.binary_fold(op_or, val))

    add_collision(ored)
    std.concat

    return any(collision_masks)


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

    @pyeval
    def get_row(self, nr):
        return [self.cells[GRID_SIZE * nr + idx].options for idx in range(GRID_SIZE)]

    @pyeval
    def get_column(self, nr):
        return [self.cells[nr + GRID_SIZE * idx].options for idx in range(GRID_SIZE)]

    @pyeval
    def get_block(self, nr):
        return [self.cells[idx].options for idx in self._block_indicies(nr)]

    def gen_next(self):
        bf = std.binary_fold

        rows = [self.get_row(nr) for nr in range(GRID_SIZE)]
        cols = [self.get_column(nr) for nr in range(GRID_SIZE)]
        blks = [self.get_block(nr) for nr in range(GRID_SIZE)]

        row_masks = [bf(op_or, row) for row in rows]
        col_masks = [bf(op_or, col) for col in cols]
        blk_masks = [bf(op_or, blk) for blk in blks]

        any_invalid = any([contains_duplicates(group) for group in rows + cols + blks])

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

        valid_cnt = [
            (elem[3], Unsigned.upto(CELL_CNT)(nr))
            for nr, elem in enumerate(update_result)
        ]

        return (
            any_invalid,
            any(cell_changed),
            Sudoku(cells=cell_updates),
            cell_valid,
            std.batched_fold(min_pair, valid_cnt)[1],
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
    dbg_maxsize = Port.output(Unsigned[8], default=Null)

    def architecture(self):
        ctx = std.SequentialContext(
            std.Clock(self.clk), attributes={"zero_init_temporaries": True}
        )

        current_sudoku = std.Signal[SudokuPos]()
        next_sudoku = std.Signal[Sudoku]()
        invalid = Signal[Bit]()
        changes = Signal[Bit]()
        next_guess = Signal[BitVector[GRID_SIZE]](Null)
        next_idx = Signal[Unsigned.upto(CELL_CNT)](Null)

        @std.concurrent(attributes={"zero_init_temporaries": True})
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

        @ctx
        async def proc_solve():
            nonlocal current_sudoku, next_sudoku, invalid
            self.dbg_a <<= 0
            self.dbg_size <<= 0
            self.dbg_maxsize <<= 0
            await self.start
            self.dbg_a <<= 1

            inp_sudoku = std.from_bits[Sudoku](self.data_inp)

            current_sudoku.cells <<= inp_sudoku.cells
            current_sudoku.guess <<= std.one_hot(GRID_SIZE, 0)

            stack = std.Stack[SudokuPos, 12](mode=std.StackMode.DROP_OLD)

            is_done = cohdl.always(current_sudoku.is_done())

            while True:
                stack_size = stack.size()
                self.dbg_size <<= stack_size
                self.dbg_maxsize <<= (
                    stack_size if stack_size > self.dbg_maxsize else self.dbg_maxsize
                )

                if invalid or (not is_done and not changes and next_guess == Null):
                    self.dbg_a <<= 2
                    if stack.empty():
                        self.done ^= True
                        self.valid ^= False
                        break
                    else:
                        current_sudoku <<= stack.pop()

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


from cohdl_sim import Simulator


sim = Simulator(
    SudokuSolver,
    sim_args=["--vcd=waveform.vcd"],
    # no_build_update=True,
    # additional_vhdl=["build/vhdl/SudokuSolver.vhd"],
)

sudoku_1 = [
    [0, 6],
    [0, 9, 7, 2, 5, 4],
    [3, 4, 0, 0, 0, 0, 9, 1],
    #
    [0, 0, 6, 0, 4, 0, 8, 0, 1],
    [0, 0, 0, 7, 0, 0, 3],
    [0, 0, 0, 8, 0, 1, 2, 5, 6],
    #
    [0, 0, 5, 0, 7],
    [0, 0, 0, 5, 0, 0, 7],
    [0, 3, 0, 1, 0, 2, 5, 9],
]

sudoku_2 = [
    [0, 0, 0, 0, 0, 6, 0, 7, 0],
    [0, 0, 0, 0, 9, 0, 0, 0, 2],
    [6, 3, 0, 0, 0, 0, 0, 0, 5],
    #
    [0, 0, 0, 1, 8, 9],
    [0, 4, 0, 7],
    [0, 7, 5, 2],
    #
    [0, 0, 8],
    [7, 0, 0, 0, 0, 0, 1, 8],
    [0, 0, 1, 0, 0, 2, 9],
]

sudoku_3 = []


@sim.test
async def test_bench(dut: SudokuSolver):
    with open("sudoku.log", "w") as file:

        def log(*args, **kwargs):
            print(*args, **kwargs)
            print(*args, **kwargs, file=file)

        sim.gen_clock(dut.clk, std.GHz(1))

        def set_digit(row, col, val):
            cell = (col * GRID_SIZE) + row * CELL_CNT

            dut.data_inp[cell + GRID_SIZE - 1 : cell] <<= (
                std.one_hot(GRID_SIZE, val - 1) if val != 0 else Null
            )

        def set_all(content):
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    set_digit(row, col, 0)

            for row_nr, row in enumerate(content):
                for col_nr, val in enumerate(row):
                    set_digit(row_nr, col_nr, val)

        def get_digit(row, col):
            cell = (col * GRID_SIZE) + row * CELL_CNT

            val = dut.data_out[cell + GRID_SIZE - 1 : cell].copy()

            if val == Null:
                return 0

            for nr in range(GRID_SIZE):
                if val == std.one_hot(GRID_SIZE, nr):
                    return nr + 1

            return "X"

        def show():
            for row in range(GRID_SIZE):
                log(*[get_digit(row, col) for col in range(GRID_SIZE)])
            log()

        dut.start <<= False
        dut.data_inp <<= Null

        set_all(sudoku_1)

        await sim.clock_cycles(dut.clk, 5)

        dut.start <<= True
        show()

        for nr in range(100):
            await sim.clock_cycles(dut.clk, 1)
            dut.start <<= False
            print("---- ", nr)

            if dut.done:
                show()
                return

        await sim.clock_cycles(dut.clk, 5)

        await sim.clock_cycles(dut.clk, 10000)
        print("---------")
        show()

        for nr in range(5):
            await sim.clock_cycles(dut.clk, 1)
            dut.start <<= False
            print("---- ", nr)
            show()

            if dut.done:
                return


# vhdl = std.VhdlCompiler.to_string(SudokuSolver)
# with open("sudoku.vhdl", "w") as file:
#    print(vhdl, file=file)
std.Value
