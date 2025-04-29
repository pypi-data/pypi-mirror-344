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
from functools import lru_cache

GRID_SIZE = 9
BLOCK_SIZE = 3
CELL_CNT = 81


class TrippleEntity(cohdl.Entity):
    a = Port.input(BitVector[9])
    b = Port.input(BitVector[9])
    c = Port.input(BitVector[9])

    result = Port.output(BitVector[9])

    @pyeval
    @lru_cache
    def _result_map(self, bit_cnt: int):
        return {
            Unsigned[9](nr).bitvector: Unsigned[9](nr).bitvector
            for nr in range(2**9)
            if nr.bit_count() == bit_cnt
        }

    def architecture(self):
        @std.concurrent
        def logic():
            a = self.a
            b = self.b
            c = self.c

            a1 = std.select[BitVector[9]](
                a, self._result_map(1), default=BitVector[9](Null)
            )
            b1 = std.select[BitVector[9]](
                b, self._result_map(1), default=BitVector[9](Null)
            )
            c1 = std.select[BitVector[9]](
                c, self._result_map(1), default=BitVector[9](Null)
            )

            a2 = std.select[BitVector[9]](
                a | b, self._result_map(2), default=BitVector[9](Null)
            )
            b2 = std.select[BitVector[9]](
                b | c, self._result_map(2), default=BitVector[9](Null)
            )
            c2 = std.select[BitVector[9]](
                a | c, self._result_map(2), default=BitVector[9](Null)
            )

            a3 = std.select[BitVector[9]](
                a | b | c, self._result_map(3), default=BitVector[9](Null)
            )

            self.result <<= a1 | b1 | c1 | a2 | b2 | c2 | a3


@pyeval
@lru_cache
def _score_map():
    return {
        Unsigned[9](val).bitvector: Unsigned[4](val.bit_count() - 2)
        for val in range(2**9)
        if val.bit_count() >= 2
    }


class ScoreCell(Entity):
    options = Port.input(BitVector[9])

    score = Port.output(Unsigned[4])

    def architecture(self):
        @std.concurrent
        def logic():
            self.score <<= std.select(
                self.options, _score_map(), default=Unsigned[4](Full)
            )


class CellUpdate(Entity):
    inp_options = Port.input(BitVector[9])
    inp_solved = Port.input(Bit)

    tripple_0 = Port.input(BitVector[9])
    tripple_1 = Port.input(BitVector[9])
    tripple_2 = Port.input(BitVector[9])
    tripple_3 = Port.input(BitVector[9])
    tripple_4 = Port.input(BitVector[9])
    tripple_5 = Port.input(BitVector[9])
    tripple_6 = Port.input(BitVector[9])
    tripple_7 = Port.input(BitVector[9])

    out_changed = Port.output(Bit)
    out_invalid = Port.output(Bit)
    out_solved = Port.output(Bit)
    out_options = Port.output(BitVector[9])

    def architecture(self):
        tripples = [
            self.tripple_0,
            self.tripple_1,
            self.tripple_2,
            self.tripple_3,
            self.tripple_4,
            self.tripple_5,
            self.tripple_6,
            self.tripple_7,
        ]

        @std.concurrent
        def logic():
            not_allowed = std.batched_fold(lambda a, b: a | b, tripples)
            solved = std.is_one_hot(self.inp_options)
            options = std.cond[BitVector[GRID_SIZE]](
                solved, self.inp_options, ~not_allowed
            )

            self.out_options <<= options
            self.out_changed <<= self.inp_options != options
            self.out_invalid <<= not options and not solved
            self.out_solved <<= solved


class Cell(std.Record):
    options: BitVector[GRID_SIZE]
    solved: Bit

    def score(self):
        return std.OpenEntity[ScoreCell](options=self.options).score

    def update(self, tripples: list[BitVector[9]]) -> CellUpdate:
        return std.OpenEntity[CellUpdate](
            inp_options=self.options,
            inp_solved=self.solved,
            tripple_0=tripples[0],
            tripple_1=tripples[1],
            tripple_2=tripples[2],
            tripple_3=tripples[3],
            tripple_4=tripples[4],
            tripple_5=tripples[5],
            tripple_6=tripples[6],
            tripple_7=tripples[7],
        )


class Sudoku(std.Record):
    cells: std.Array[Cell, CELL_CNT]
    guess: BitVector[9]

    def next_idx(self):
        return std.min_index(self.cells, key=lambda cell: cell.score())

    @staticmethod
    def from_vec(inp: BitVector[CELL_CNT * GRID_SIZE]):
        return Sudoku(
            cells=[
                Cell(inp[v + 8 : v], False) for v in range(0, CELL_CNT * GRID_SIZE, 9)
            ],
            guess=std.one_hot(9, 0),
        )

    def to_vec(self):
        return std.concat(*[cell.options for cell in self.cells])

    @pyeval
    def _cell_by_coord(self, row, col):
        idx = row * 9 + col
        return self.cells[idx].options

    @pyeval
    def _gen_tripples(self) -> list[tuple[Cell, list[BitVector[9]]]]:
        rt = row_tripples = []
        ct = col_tripples = []

        for n in range(9):
            row_tripples.append(
                [
                    std.OpenEntity[TrippleEntity](
                        a=self._cell_by_coord(n, off + 0),
                        b=self._cell_by_coord(n, off + 1),
                        c=self._cell_by_coord(n, off + 2),
                    ).result
                    for off in (0, 3, 6)
                ]
            )

            col_tripples.append(
                [
                    std.OpenEntity[TrippleEntity](
                        a=self._cell_by_coord(off + 0, n),
                        b=self._cell_by_coord(off + 1, n),
                        c=self._cell_by_coord(off + 2, n),
                    ).result
                    for off in (0, 3, 6)
                ]
            )

        result = []

        for cell_id in range(CELL_CNT):
            row = cell_id // 9
            col = cell_id % 9

            blk_x, blk_xoff = divmod(col, 3)
            blk_y, blk_yoff = divmod(row, 3)

            result.append(
                (
                    self.cells[cell_id],
                    (
                        *[rt[row][i] for i in (0, 1, 2) if i != blk_x],
                        *[ct[col][i] for i in (0, 1, 2) if i != blk_y],
                        *[rt[blk_y * 3 + i][blk_x] for i in (0, 1, 2) if i != blk_yoff],
                        *[ct[blk_x * 3 + i][blk_y] for i in (0, 1, 2) if i != blk_xoff],
                    ),
                )
            )

        return result

    def step(self):
        update_result = [
            cell.update(tripplets) for cell, tripplets in self._gen_tripples()
        ]

        return (
            any([val.out_changed for val in update_result]),
            any([val.out_invalid for val in update_result]),
            all([val.out_solved for val in update_result]),
            Sudoku(
                cells=[Cell(val.out_options, val.out_solved) for val in update_result],
                guess=self.guess,
            ),
        )


#
#
#


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

    dbg_next_valid = Port.output(BitVector[9], default=Null)
    dbg_next_idx = Port.output(Unsigned[8], default=Null)
    dbg_next_guess = Port.output(BitVector[9], default=Null)

    def architecture(self):
        ctx = std.SequentialContext(std.Clock(self.clk))

        current_sudoku = std.Signal[Sudoku]()
        next_sudoku = std.Signal[Sudoku]()
        invalid = Signal[Bit]()
        changes = Signal[Bit]()
        next_guess = Signal[BitVector[GRID_SIZE]](Null)
        next_idx = Signal[Unsigned.upto(CELL_CNT)](Null)
        solved = std.Signal[Bit](Null)

        @std.concurrent
        def logic_update():
            nonlocal next_sudoku, invalid, changes, next_guess, next_idx, solved

            update_result = current_sudoku.step()

            changes <<= update_result[0]
            invalid <<= update_result[1]
            solved <<= update_result[2]
            next_sudoku <<= update_result[3]

            next_idx <<= current_sudoku.next_idx()

            next_valid = current_sudoku.cells.get_elem(next_idx, std.Value).options

            next_guess <<= std.choose_first(
                *[
                    (
                        next_valid & (current_sudoku.guess.unsigned << nr).bitvector,
                        (current_sudoku.guess.unsigned << nr),
                    )
                    for nr in range(GRID_SIZE)
                ],
                default=Null,
            )

            self.data_out <<= current_sudoku.to_vec()

            self.dbg_solved_cnt <<= std.count(
                current_sudoku.cells, check=lambda x: bool(x.options)
            )

            self.dbg_next_idx <<= next_idx
            self.dbg_next_valid <<= next_valid
            self.dbg_next_guess <<= next_guess

        @ctx
        async def proc_solve():
            nonlocal current_sudoku, next_sudoku, invalid
            self.dbg_a <<= 0
            self.dbg_size <<= 0
            await self.start
            self.dbg_a <<= 1

            current_sudoku <<= Sudoku.from_vec(self.data_inp)
            stack = std.Stack[Sudoku, CELL_CNT]()

            while True:
                self.dbg_size <<= stack.size()
                if invalid or (not solved and not changes and next_guess == Null):
                    self.dbg_a <<= 2
                    if stack.empty():
                        self.done ^= True
                        self.valid ^= False
                        break
                    else:
                        temp_guess = stack.pop()
                        current_sudoku <<= temp_guess

                elif solved:
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
                        Sudoku(
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


sim = Simulator(SudokuSolver, sim_args=["--vcd=waveform.vcd"], use_build_cache=False)


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

        file_path = "/home/alexander/dev/tmp/tdoku/data/puzzles3_magictour_top1465"
        file_path = "/home/alexander/dev/tmp/tdoku/data/puzzles6_forum_hardest_1106"
        file_path = "/home/alexander/dev/tmp/tdoku/data/puzzles5_forum_hardest_1905_11+"

        with open(file_path) as file:
            nr = 0
            total = 0
            STOP_NR = 25
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue

                if nr >= STOP_NR:
                    break

                nr += 1
                assert len(line) == 81, f"invalid line length: '{line}'"

                if False:
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

                    if _ < 10 and False:
                        print(" XXXXX ", dut.dbg_size, dut.dbg_solved_cnt, dut.dbg_a)
                        print(f"{dut.dbg_next_idx=}")
                        print(f"{dut.dbg_next_valid=}")
                        print(f"{dut.dbg_next_guess=}")
                        show()
                        print()

                    if dut.done:
                        total += _
                        print(
                            " DONE ",
                            f"{_:4}",
                            f"{_*0.01:6.2f} us",
                            f"{_*0.02:6.2f} us",
                            f"{_*0.03:6.2f} us",
                        )

                        if False:
                            print(
                                " DONE ", _, dut.dbg_size, dut.dbg_solved_cnt, dut.dbg_a
                            )
                            print(f"{dut.dbg_next_idx=}")
                            print(f"{dut.dbg_next_valid=}")
                            print(f"{dut.dbg_next_guess=}")
                            show()
                            print()
                        break
                        # return
                else:
                    print("Solver failed")
                    print()

                    show()

                    return

            total /= STOP_NR
            print(
                " TOTAL ",
                f"{total:4}",
                f"{total*0.01:6.2f} us",
                f"{total*0.02:6.2f} us",
                f"{total*0.03:6.2f} us",
            )
