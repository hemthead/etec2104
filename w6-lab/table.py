from typing import ClassVar, NamedTuple, SupportsIndex
import sys

# Box drawing characters
BOX_H = '-' # horizontal
BOX_V = '|' # vertical
BOX_UL = '+' # upper left
BOX_UM = '+' # upper middle
BOX_UR = '+' # upper right
BOX_ML = '+' # middle left
BOX_MM = '+' # middle middle
BOX_MR = '+' # middle right
BOX_BL = '+' # bottom left
BOX_BM = '+' # bottom middle
BOX_BR = '+' # bottom right

# Terminal color sequences
COLOR_RST = ''

# fancy unicode + colored output in-tty
if sys.stdout.isatty():
    BOX_H = '─'
    BOX_V = '│'
    BOX_UL = '┌'
    BOX_UR = '┐'
    BOX_UM = '┬'
    BOX_MM = '┼'
    BOX_ML = '├'
    BOX_MR = '┤'
    BOX_BL = '└'
    BOX_BR = '┘'
    BOX_BM = '┴'

    COLOR_RST = '\033[0m'

class Table:
    Color = str
    """An ANSI escape sequnce."""

    class RowItem(NamedTuple):
        value: object
        formatting: str
        color: Table.Color

    def __init__(self, title: str | None = None):
        self.title: str | None = title
        self.row_idx: int = 0
        self.cell_idx: int = 0
        self.rows: list[list[Table.RowItem]] = list()
        self.rows.append(list())
        self.widths: list[int] = list()


    Char = str
    """Single unicode grapheme (occupies one cell in terminal)."""

    @staticmethod
    #  w[0] w[1]
    # +----+----+
    # l    m    r
    def _sep_line(l: Char, m: Char, r: Char, widths: list[int]) -> str:
        line = l
        for i, w in enumerate(widths):
            line += BOX_H*(w+2)
            if i != len(widths) - 1:
                line += m
        line += r
        return line

    def add_val(self, val: object, formatting="", width=None, color=""):
        if width is None:
            width = len(f'{val:{formatting}}')

        if self.row_idx == 0:
            self.widths.append(width)

        row_item = Table.RowItem(val, formatting, color);
        self.rows[self.row_idx].append(row_item)
        self.widths[self.cell_idx] = max(self.widths[self.cell_idx], width)

        self.cell_idx += 1

    def finish_row(self):
        self.rows.append(list())
        self.row_idx += 1
        self.cell_idx = 0

    def print(self):
        if self.title is not None:
            # widths of each cell + fenceposting the three spaces between cell_values (2 padding, 1
            # border)
            width = sum(self.widths) + 3*(len(self.widths) - 1)
            print(Table._sep_line(BOX_UL, BOX_H, BOX_UR, self.widths))
            print(f'{BOX_V} {self.title:^{width}} {BOX_V}')
            print(Table._sep_line(BOX_ML, BOX_UM, BOX_MR, self.widths))
        else:
            print(Table._sep_line(BOX_UL, BOX_UM, BOX_UR, self.widths))


        # last row is empty
        for idx, row in enumerate(self.rows[:-1]):
            if idx != 0:
                print(Table._sep_line(BOX_ML, BOX_MM, BOX_MR, self.widths))
            print(BOX_V, end="")
            for cell_i, cell in enumerate(row):
                width = self.widths[cell_i]
                fmt = cell.formatting
                color = cell.color if sys.stdout.isatty() else ''
                # this could be made maybe more appropriate by replacing 'w' or something in `fmt`
                # with width if `fmt` is present...
                print(f' {color}{cell.value:{width}{fmt}}{COLOR_RST if color != '' else ''} {BOX_V}',
                      end="")
            print()

        print(Table._sep_line(BOX_BL, BOX_BM, BOX_BR, self.widths))

if __name__ == "__main__":
    test = Table("Secret")
    test.add_val("col_1")
    test.add_val("col_2")
    test.finish_row()

    test.add_val(1)
    test.add_val(2.32, '.3f')
    test.finish_row()

    test.add_val("string")
    test.add_val(complex(1,3))
    test.finish_row()

    test.print()
