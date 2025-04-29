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

sys.setrecursionlimit(10000)

# cohdl.use_pretty_traceback(False)


class Stack:
    def __init__(self, T, depth):
        self._mem = std.Array[T, depth]()
        self._cnt = std.Signal[Unsigned.upto(depth)](0)
        self._depth = depth

    def push(self, data):
        assert self._cnt < self._depth, "push to full stack"

        self._mem.set_elem(self._cnt, data)
        self._cnt <<= self._cnt + 1

    def pop(self):
        assert self._cnt != 0, "pop from empty stack"

        self._cnt <<= self._cnt - 1
        return self._mem.get_elem(self._cnt - 1, qualifier=std.Value)

    def empty(self):
        return self._cnt == 0

    def full(self):
        return self._cnt == self._depth

    def clear(self):
        self._cnt <<= 0


class Cell(std.Record):
    options: BitVector[9]

    def __bool__(self):
        return bool(self.options)

    def solved(self):
        return bool(self.options)

    def solve_one(self, invalid_mask: BitVector[9]):
        valid_mask = ~invalid_mask

        found_solution = std.is_one_hot(valid_mask | self.options)

        if found_solution:
            self.options <<= valid_mask

        return found_solution

    def gen_next(self, invalid_mask: BitVector[9]):
        valid_mask = ~invalid_mask

        found_solution = std.is_one_hot(valid_mask | self.options)

        return (
            Cell(options=valid_mask if found_solution else Null),
            found_solution,
            valid_mask,
        )


op_or = lambda a, b: a | b
op_and = lambda a, b: a & b


def contains_duplicates(inp: list[BitVector[9]]):
    collision_masks = []
    ored = []

    def add_collision(inp):
        a, b, c = inp
        # collision_masks.append((a & b) | (a & c) | (b & c))

        std.as_pyeval(list.append, collision_masks, (a & b) | (a & c) | (b & c))

    for a in (0, 3, 6):
        add_collision(inp[a : a + 3])
        # ored.append(inp[a] | inp[a + 1] | inp[a + 2])

        std.as_pyeval(list.append, ored, inp[a] | inp[a + 1] | inp[a + 2])

    add_collision(ored)

    return any(collision_masks)


class Sudoku(std.Record):
    cells: std.Array[Cell, 81]

    def is_done(self):
        return all(self.cells)

    def next_idx(self):
        return std.choose_first[Unsigned[7]](
            *[
                (not cell.solved(), Unsigned[7](nr))
                for nr, cell in enumerate(self.cells)
            ],
            default=Unsigned[7](Full),
        )

    def get_row(self, nr):
        return [self.cells[9 * nr + idx].options for idx in range(9)]

    def get_column(self, nr):
        return [self.cells[nr + 9 * idx].options for idx in range(9)]

    def get_block(self, nr):
        block_x = nr % 3
        block_y = nr // 3

        start_idx = block_y * 9 * 3 + block_x * 3
        indices = [start_idx + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)]

        return [self.cells[idx].options for idx in indices]

    def gen_next(self):

        bf = std.binary_fold

        row_masks = [bf(op_or, self.get_row(nr)) for nr in range(9)]
        col_masks = [bf(op_or, self.get_column(nr)) for nr in range(9)]
        blk_masks = [bf(op_or, self.get_block(nr)) for nr in range(9)]

        row_invalid = [contains_duplicates(self.get_row(nr)) for nr in range(9)]
        col_invalid = [contains_duplicates(self.get_column(nr)) for nr in range(9)]
        blk_invalid = [contains_duplicates(self.get_block(nr)) for nr in range(9)]

        any_invalid = any(row_invalid) or any(col_invalid) or any(blk_invalid)

        def update_cell(idx: int):
            row = idx // 9
            col = idx % 9
            blk = (row // 3) + (col // 3) * 3

            return self.cells[idx].gen_next(
                row_masks[row] | col_masks[col] | blk_masks[blk]
            )

        update_result = [update_cell(idx) for idx in range(81)]

        cell_updates = [elem[0] for elem in update_result]
        cell_changed = [elem[1] for elem in update_result]
        cell_valid = [elem[2] for elem in update_result]

        return any_invalid, any(cell_changed), Sudoku(cells=cell_updates), cell_valid


class SudokuPos(Sudoku):
    pos: Unsigned[7]
    guess: BitVector[9]

    def next_guess(self, *, next_pos=None) -> SudokuPos:
        if next_pos is not None:
            pos = next_pos
        else:
            pos = self.pos

        new_cells = std.Variable(self.cells)
        std.assign(new_cells[pos].options, self.guess)
        return SudokuPos(new_cells, pos, self.guess.unsigned << 1)


class SudokuSolver(Entity):
    clk = Port.input(Bit)

    start = Port.input(Bit)
    data_inp = Port.input(BitVector[9 * 9 * 9])
    data_out = Port.output(BitVector[9 * 9 * 9])

    done = Port.output(Bit, default=False)
    valid = Port.output(Bit, default=False)

    dbg_a = Port.output(Unsigned[3], default=Null)

    def architecture(self):
        ctx = std.SequentialContext(std.Clock(self.clk))

        current_sudoku = std.Signal[SudokuPos]()
        next_sudoku = std.Signal[Sudoku]()
        invalid = Signal[Bit]()
        changes = Signal[Bit]()
        prev_pop = Signal[bool](False)
        next_guess = Signal[BitVector[9]](Null)

        @std.concurrent
        def logic_update():
            nonlocal next_sudoku, invalid, changes, next_guess

            update_result = current_sudoku.gen_next()

            invalid <<= update_result[0]
            changes <<= update_result[1]
            next_sudoku <<= update_result[2]

            cells_valid = std.concat(update_result[3][::-1])
            cell_valid = std.select_batch(
                cells_valid, std.one_hot(81, current_sudoku.pos), 9
            )

            next_guess <<= std.choose_first(
                *[
                    (
                        cell_valid & (current_sudoku.guess.unsigned << nr),
                        (current_sudoku.guess.unsigned << nr),
                    )
                    for nr in range(9)
                ],
                default=Null,
            )

            self.data_out <<= std.to_bits(current_sudoku.cells)

        @ctx
        async def proc_solve():
            nonlocal current_sudoku, next_sudoku, invalid, prev_pop
            self.dbg_a <<= 0
            await self.start
            self.dbg_a <<= 1

            inp_sudoku = std.from_bits[Sudoku](self.data_inp)

            current_sudoku.cells <<= inp_sudoku.cells
            current_sudoku.pos <<= inp_sudoku.next_idx()
            current_sudoku.guess <<= std.one_hot(9, 0)

            stack = Stack(SudokuPos, 90)

            while True:
                if invalid:
                    self.dbg_a <<= 2
                    if stack.empty():
                        self.done ^= True
                        self.valid ^= False
                        break
                    else:
                        temp_guess = stack.pop().next_guess()
                        prev_pop ^= True
                        current_sudoku <<= temp_guess

                        if temp_guess.guess == Null:
                            break

                elif current_sudoku.is_done():
                    self.dbg_a <<= 3
                    self.done ^= True
                    self.valid ^= True
                    break

                elif changes:
                    self.dbg_a <<= 4

                    current_sudoku.cells <<= next_sudoku.cells

                else:
                    self.dbg_a <<= 5

                    next_idx = current_sudoku.next_idx()
                    next_guess = current_sudoku.next_guess(next_pos=next_idx)

                    if prev_pop:
                        stack.push(current_sudoku)
                        current_sudoku.pos <<= next_idx
                    else:
                        stack.push(next_guess)
                        current_sudoku.pos <<= next_guess.next_idx()

                    current_sudoku <<= next_guess
                    current_sudoku.guess <<= std.one_hot(9, 0)


from cohdl_sim import Simulator


sim = Simulator(SudokuSolver, sim_args=["--vcd=waveform.vcd"])


@sim.test
async def test_bench(dut: SudokuSolver):
    with open("sudoku.log", "w") as file:

        def log(*args, **kwargs):
            print(*args, **kwargs)
            print(*args, **kwargs, file=file)

        sim.gen_clock(dut.clk, std.MHz(100))

        def set_digit(row, col, val):
            cell = (col * 9) + row * 81
            dut.data_inp[cell + 8 : cell] <<= std.one_hot(9, val - 1)

        def get_digit(row, col):
            cell = (col * 9) + row * 81

            val = dut.data_out[cell + 8 : cell]

            if val == Null:
                return 0

            for nr in range(9):
                if val == std.one_hot(9, nr):
                    return nr + 1

            return "X"

        def show():
            for row in range(9):
                log(*[get_digit(row, col) for col in range(9)])
            log()

        dut.start <<= False
        dut.data_inp <<= Null
        # dut.data_inp[0] <<= True
        # dut.data_inp[9] <<= True

        await sim.clock_cycles(dut.clk, 5)

        dut.start <<= True
        show()

        for _ in range(25):
            await sim.clock_cycles(dut.clk, 1)
            show()

        await sim.clock_cycles(dut.clk, 5)
        show()

        await sim.clock_cycles(dut.clk, 1000)


# vhdl = std.VhdlCompiler.to_string(SudokuSolver)
# with open("sudoku.vhdl", "w") as file:
#    print(vhdl, file=file)
