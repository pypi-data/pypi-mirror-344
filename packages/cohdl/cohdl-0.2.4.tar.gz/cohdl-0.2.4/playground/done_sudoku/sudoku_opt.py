from __future__ import annotations

import cohdl
from cohdl import std
from cohdl import Bit, BitVector, Unsigned, Port, Signal, Entity, pyeval, Null, Full

GRID_SIZE = 9
BLOCK_SIZE = 3
CELL_CNT = 81


class ScoreCell(Entity):
    prev_state = Port.input(BitVector[GRID_SIZE])
    valid_mask = Port.input(BitVector[GRID_SIZE])

    score = Port.output(Unsigned[3])
    found_solution = Port.output(Bit)
    new_state = Port.output(BitVector[GRID_SIZE])

    def architecture(self):
        assert GRID_SIZE == 9

        def score_result(bit_cnt):
            assert 0 <= bit_cnt <= 9

            if bit_cnt < 2:
                result = 7
            else:
                result = bit_cnt - 2

            return (Unsigned[3](result), bit_cnt == 1)

        score_map = {
            Unsigned[3](a) @ Unsigned[3](b): score_result(a.bit_count() + b)
            for a in range(8)
            for b in range(7)
        }

        @std.concurrent
        def logic():
            already_solved = bool(self.prev_state)

            level_1 = std.count_set_bits(self.valid_mask[5:0], batch_size=6)

            score, new_solution = (
                (Full, False)
                if already_solved
                else std.select(
                    self.valid_mask[8:6] @ level_1, score_map, default=(Full, False)
                )
            )

            self.score <<= score
            self.found_solution <<= new_solution
            self.new_state <<= self.valid_mask if new_solution else self.prev_state


class ScoreCellNew(Entity):
    prev_state = Port.input(BitVector[GRID_SIZE])
    invalid_mask = Port.input(BitVector[GRID_SIZE])

    new_state = Port.output(BitVector[GRID_SIZE])
    new_solution = Port.output(Bit)
    valid_solution = Port.output(BitVector[GRID_SIZE])
    valid_cnt = Port.output(Unsigned[4])

    def architecture(self):

        @std.concurrent
        def logic():
            valid_mask = ~self.invalid_mask

            found_solution = False if self.prev_state else std.is_one_hot(valid_mask)

            self.new_state <<= valid_mask if found_solution else self.prev_state
            self.new_solution <<= found_solution
            self.valid_solution <<= valid_mask
            self.valid_cnt <<= std.count_set_bits(
                valid_mask
                if not (found_solution or self.prev_state)
                else std.ones(GRID_SIZE)
            )


class CmpScore(Entity):
    a = Port.input(BitVector[3])
    b = Port.input(BitVector[3])

    result = Port.output(Bit)

    def architecture(self):
        result_map = {
            Unsigned[3](a) @ Unsigned[3](b): Bit(a < b)
            for a in range(7)
            for b in range(7)
        }

        @std.concurrent
        def logic():
            self.result <<= std.select(self.a @ self.b, result_map, default=Null)


class CellUpdate:
    def __init__(
        self,
        new_state: BitVector,
        new_solution: bool,
        valid_solutions: BitVector,
        valid_cnt: Unsigned,
    ):
        self.new_state = new_state
        self.new_solution = new_solution
        self.valid_solution = valid_solutions
        self.valid_cnt = valid_cnt

    @staticmethod
    def new(state: BitVector[GRID_SIZE], invalid_mask: BitVector[GRID_SIZE]):
        entity = std.OpenEntity[ScoreCellNew](
            prev_state=state, invalid_mask=invalid_mask
        )

        return CellUpdate(
            new_state=entity.new_state,
            new_solution=entity.new_solution,
            valid_solutions=entity.valid_solution,
            valid_cnt=entity.valid_cnt,
        )


class SudokuUpdate:
    def __init__(
        self,
        invalid: bool,
        any_update: bool,
        new_state: Sudoku,
        valid_solutions: list[BitVector],
        next_idx: Unsigned,
    ):
        self.invaid = invalid
        self.any_update = any_update
        self.new_state = new_state
        self.valid_solutions = valid_solutions
        self.next_idx = next_idx


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
    return any(collision_masks)


class Sudoku(std.Record):
    cells: std.Array[BitVector[GRID_SIZE], CELL_CNT]

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
        return [self.cells[GRID_SIZE * nr + idx] for idx in range(GRID_SIZE)]

    @pyeval
    def get_column(self, nr):
        return [self.cells[nr + GRID_SIZE * idx] for idx in range(GRID_SIZE)]

    @pyeval
    def get_block(self, nr):
        return [self.cells[idx] for idx in self._block_indicies(nr)]

    def gen_next(self):
        bf = std.binary_fold

        rows = [self.get_row(nr) for nr in range(GRID_SIZE)]
        cols = [self.get_column(nr) for nr in range(GRID_SIZE)]
        blks = [self.get_block(nr) for nr in range(GRID_SIZE)]

        row_masks = [bf(op_or, row) for row in rows]
        col_masks = [bf(op_or, col) for col in cols]
        blk_masks = [bf(op_or, blk) for blk in blks]

        def update_cell(idx: int):
            row = idx // GRID_SIZE
            col = idx % GRID_SIZE
            blk = (row // BLOCK_SIZE) * BLOCK_SIZE + (col // BLOCK_SIZE)

            return CellUpdate.new(
                self.cells[idx], row_masks[row] | col_masks[col] | blk_masks[blk]
            )

        update_result = [update_cell(idx) for idx in range(CELL_CNT)]

        return SudokuUpdate(
            invalid=any([contains_duplicates(group) for group in rows + cols + blks]),
            any_update=any([elem.new_solution for elem in update_result]),
            new_state=Sudoku(cells=[elem.new_state for elem in update_result]),
            valid_solutions=[elem.valid_solution for elem in update_result],
            next_idx=std.min_index(update_result, key=lambda x: x.valid_cnt),
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

    dbg_size = Port.output(Unsigned[8], default=Null)
    dbg_maxsize = Port.output(Unsigned[8], default=Null)
    dbg_steps = Port.output(Unsigned[8], default=Null)

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

            invalid <<= update_result.invaid
            changes <<= update_result.any_update
            next_sudoku <<= update_result.new_state
            next_idx <<= update_result.next_idx

            cells_valid = std.concat(*update_result.valid_solutions[::-1])
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
            await self.start
            self.dbg_size <<= 0
            self.dbg_maxsize <<= 0
            self.dbg_steps <<= 0

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
                self.dbg_steps <<= self.dbg_steps + 1

                if invalid or (not is_done and not changes and next_guess == Null):
                    if stack.empty():
                        self.done ^= True
                        self.valid ^= False
                        break
                    else:
                        current_sudoku <<= stack.pop()

                elif is_done:
                    self.done ^= True
                    self.valid ^= True
                    break

                elif changes:
                    current_sudoku.cells <<= next_sudoku.cells

                else:
                    stack.push(
                        SudokuPos(
                            current_sudoku.cells,
                            next_guess.unsigned << 1,
                        )
                    )

                    current_sudoku.cells[next_idx] <<= next_guess
                    current_sudoku.guess <<= std.one_hot(GRID_SIZE, 0)


# cohdl.use_pretty_traceback(False)
# std.VhdlCompiler.to_string(SudokuSolver)
# exit()

#
#
#
#
#
#
#
#
#


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
            dut.data_inp[cell + GRID_SIZE - 1 : cell] <<= (
                std.one_hot(GRID_SIZE, val - 1) if val != 0 else Null
            )

        def set_all(content):
            for cell_nr, val in enumerate(content):
                set_digit(cell_nr, val)

        def get_digit(row, col):
            cell = (col * GRID_SIZE) + row * CELL_CNT

            val = dut.data_out[cell + GRID_SIZE - 1 : cell].copy()

            if val == Null:
                return 0

            for nr in range(GRID_SIZE):
                if val == std.one_hot(GRID_SIZE, nr):
                    return nr + 1

            return "."

        def show():
            for row in range(GRID_SIZE):
                log(*[get_digit(row, col) for col in range(GRID_SIZE)])
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

                for _ in range(1000):
                    await sim.rising_edge(dut.clk)
                    dut.start <<= False

                    if dut.done:
                        maxsize = dut.dbg_maxsize.copy().to_int()
                        steps = dut.dbg_steps.copy().to_int()
                        duration = steps * (1 / 30)

                        print(
                            f"{dut.done=}, {dut.valid=}, {maxsize=}, {steps=}, {duration=}us"
                        )
                        show()
                        print()
                        break
                else:
                    print("Solver failed")
                    print()

                    show()

                    return
