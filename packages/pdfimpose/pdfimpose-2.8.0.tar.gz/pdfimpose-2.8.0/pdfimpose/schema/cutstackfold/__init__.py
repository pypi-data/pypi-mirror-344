# Copyright 2011-2025 Louis Paternault
#
# This file is part of pdfimpose.
#
# Pdfimpose is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pdfimpose is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfimpose.  If not, see <https://www.gnu.org/licenses/>.

"""Print pages, to be cut, stacked, folded, and eventually bound.

Example: You want to print and bind one single tiny A7 book.  This book is made with A6 sheets (when you open the book, you get two A7 pages side-by-side, which is A6).  Since you can fit four A6 pages on an A4 page, this means that you can print four A6 sheets on one A4 sheet.

To use this schema (without using option --group):

- print your imposed file, two-sided;
- cut the stack of paper, to get several stacks (four in the example above);
- stack the several stacks you got on top of each other
  (take care to keep the pages in the right order);
- fold and bind the stack of paper you got;
- voilà! You now have a shiny, tiny book.

With option --group=3 (for instance), repeat the step above for every group of three sheets. You get several signatures, that you have to bind together to get a proper book.
"""  # pylint: disable=line-too-long

import dataclasses
import decimal
import io
import itertools
import math
import numbers
import pathlib
import typing
from collections.abc import Sequence

import papersize

from .. import (
    BIND2ANGLE,
    DEFAULT_PAPER_SIZE,
    AbstractImpositor,
    Matrix,
    Page,
    nocreep,
    pdf,
    size2signature,
)


@dataclasses.dataclass
class CutStackFoldImpositor(AbstractImpositor):
    """Perform imposition of source files, with the 'cutstackfold' schema."""

    bind: str = "left"
    creep: typing.Callable[[int], float] = dataclasses.field(default=nocreep)
    imargin: str | numbers.Real | decimal.Decimal = 0
    signature: tuple[int] = (0, 0)
    group: int = 0

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.imargin, decimal.Decimal):
            self.imargin = float(self.imargin)
        elif isinstance(self.imargin, str):
            self.imargin = float(papersize.parse_length(self.imargin))

    def blank_page_number(self, source):
        pagesperpage = 4 * self.signature[0] * self.signature[1]
        if source % pagesperpage == 0:
            return 0
        return pagesperpage - (source % pagesperpage)

    def margins(self, x, y):
        """Compute and return margin for page at coordinate (x, y)."""
        margins = {
            "top": self.omargin.top if y == 0 else self.imargin / 2,
            "bottom": (
                self.omargin.bottom if y == self.signature[1] - 1 else self.imargin / 2
            ),
            "left": 0 if x % 2 == 1 else self.imargin / 2,
            "right": 0 if x % 2 == 0 else self.imargin / 2,
        }

        # Output margins
        if x == 0:
            margins["left"] = self.omargin.left
        if x == 2 * self.signature[0] - 1:
            margins["right"] = self.omargin.right

        return margins

    def base_matrix(self, total):
        """Yield a single matrix.

        This matrix contains the arrangement of source pages on the output pages.

        :param int total: Total number of source pages.
        """
        stack = total // (2 * self.signature[0] * self.signature[1])

        for inner in range(stack // 2):
            recto, verso = (
                [
                    [None for _ in range(self.signature[1])]
                    for _ in range(2 * self.signature[0])
                ]
                for _ in range(2)
            )

            for i, coord in enumerate(itertools.product(*map(range, self.signature))):
                x, y = coord
                recto[2 * x][y] = Page(
                    total - i * stack - 2 * inner - 1, **self.margins(2 * x, y)
                )
                recto[2 * x + 1][y] = Page(
                    i * stack + 2 * inner, **self.margins(2 * x + 1, y)
                )
                verso[2 * self.signature[0] - 2 * x - 1][y] = Page(
                    total - i * stack - 2 * inner - 2,
                    **self.margins(2 * self.signature[0] - 2 * x - 1, y),
                )
                verso[2 * self.signature[0] - 2 * x - 2][y] = Page(
                    i * stack + 2 * inner + 1,
                    **self.margins(2 * self.signature[0] - 2 * x - 2, y),
                )

            yield Matrix(recto, rotate=BIND2ANGLE[self.bind])
            yield Matrix(verso, rotate=BIND2ANGLE[self.bind])

    def _max_creep(self, total):
        """Return the maximum creep of the document.

        :param int total: Total number of source pages.
        """
        return max(self.creep(n) for n in range(total // 4))

    def matrixes(self, pages: int):
        pages_per_sheet = 4 * self.signature[0] * self.signature[1]
        assert pages % pages_per_sheet == 0

        if self.group == 0:
            group = math.ceil(pages / pages_per_sheet)
        else:
            group = self.group

        # Compute maximum creep
        maxcreep = self._max_creep(group * pages_per_sheet)

        # First, we compute the first group of pages
        group_matrixes = []

        for number, matrix in enumerate(self.base_matrix(group * pages_per_sheet)):
            for x, y in matrix.coordinates():
                # Number of (output) sheets stacked on top in the current (output) sheet
                included = group - number // 2 - 1
                # Number of stacks included in the current page, once cut
                stacks = self.signature[1] * (1 - x // 2) + self.signature[0] - y
                creep = self.creep(included + stacks * group)

                if number % 2 == 1:
                    # Pages are reversed on the back of sheets (odd pages)
                    x = matrix.width - x - 1

                if x % 2 == 0:
                    matrix[x, y].left += (maxcreep - creep) / 2
                    matrix[x, y].right += creep / 2
                else:
                    matrix[x, y].left += creep / 2
                    matrix[x, y].right += (maxcreep - creep) / 2
            group_matrixes.append(matrix)

        # Then, we repeat the group as many times as necessary
        for i in range(math.ceil(pages / (group * pages_per_sheet))):
            for matrix in group_matrixes:
                yield matrix.stack(i * pages_per_sheet * group)

    def crop_marks(self, *, number, total, matrix, outputsize, inputsize):
        # pylint: disable=too-many-arguments
        left, right, top, bottom = self._crop_space()
        maxcreep = self._max_creep(total)

        for x in range(self.signature[0]):
            yield (
                (
                    self.omargin.left
                    + 2 * x * inputsize[0]
                    + x * (self.imargin + maxcreep),
                    0,
                ),
                (
                    self.omargin.left
                    + 2 * x * inputsize[0]
                    + x * (self.imargin + maxcreep),
                    self.omargin.top - top,
                ),
            )
            yield (
                (
                    self.omargin.left
                    + 2 * x * inputsize[0]
                    + x * (self.imargin + maxcreep),
                    outputsize[1],
                ),
                (
                    self.omargin.left
                    + 2 * x * inputsize[0]
                    + x * (self.imargin + maxcreep),
                    outputsize[1] - self.omargin.bottom + bottom,
                ),
            )
            yield (
                (
                    self.omargin.left
                    + 2 * (x + 1) * inputsize[0]
                    + x * self.imargin
                    + (x + 1) * maxcreep,
                    0,
                ),
                (
                    self.omargin.left
                    + 2 * (x + 1) * inputsize[0]
                    + x * self.imargin
                    + (x + 1) * maxcreep,
                    self.omargin.top - top,
                ),
            )
            yield (
                (
                    self.omargin.left
                    + 2 * (x + 1) * inputsize[0]
                    + x * self.imargin
                    + (x + 1) * maxcreep,
                    outputsize[1],
                ),
                (
                    self.omargin.left
                    + 2 * (x + 1) * inputsize[0]
                    + x * self.imargin
                    + (x + 1) * maxcreep,
                    outputsize[1] - self.omargin.bottom + bottom,
                ),
            )

        for y in range(self.signature[1]):
            yield (
                (0, self.omargin.top + y * (inputsize[1] + self.imargin)),
                (
                    self.omargin.left - left,
                    self.omargin.top + y * (inputsize[1] + self.imargin),
                ),
            )
            yield ((0, self.omargin.top + (y + 1) * inputsize[1] + y * self.imargin)), (
                self.omargin.left - left,
                self.omargin.top + (y + 1) * inputsize[1] + y * self.imargin,
            )
            yield (
                (outputsize[0], self.omargin.top + y * (inputsize[1] + self.imargin)),
                (
                    outputsize[0] - self.omargin.right + right,
                    self.omargin.top + y * (inputsize[1] + self.imargin),
                ),
            )
            yield (
                (
                    outputsize[0],
                    self.omargin.top + (y + 1) * inputsize[1] + y * self.imargin,
                )
            ), (
                outputsize[0] - self.omargin.right + right,
                self.omargin.top + (y + 1) * inputsize[1] + y * self.imargin,
            )


def impose(
    files: Sequence[str | pathlib.Path | io.BytesIO],
    output: str | pathlib.Path | io.BytesIO,
    *,
    imargin=0,
    omargin=0,
    last=0,
    mark=None,
    signature=None,
    size=None,
    bind="left",
    creep=nocreep,
    group=0,
):  # pylint: disable=too-many-arguments
    """Perform imposition of source files into an output file, using the cut-stack-bind schema.

    :param Sequence[str|pathlib.Path|io.BytesIO] files: List of source files (as filenames (strings or :class:`pathlib.Path`), or :class:`io.BytesIO` streams).
    :param str | pathlib.Path | io.BytesIO output: Output file.
    :param float omargin: Output margin, in pt. Can also be a :class:`Margins` object.
    :param float imargin: Input margin, in pt.
    :param int last: Number of last pages (of the source files) to keep at the
        end of the output document.  If blank pages were to be added to the
        source files, they would be added before those last pages.
    :param list[str] mark: List of marks to add.
        Only crop marks are supported (`mark=['crop']`); everything else is silently ignored.
    :param tuple[int] signature: Layout of source pages on output pages.
        For instance ``(2, 3)`` means: the printed sheets are to be cut in a matrix of
        2 horizontal sheets per 3 vertical sheets.
        This option is incompatible with `size`.
    :param str|tuple[float] size: Size of the output page. Signature is computed to fit the page. This option is incompatible with `signature`.
    :param str bind: Binding edge. Can be one of `left`, `right`, `top`, `bottom`.
    :param function creep: Function that takes the number of sheets in argument,
        and return the space to be left between two adjacent pages
        (that is, twice the distance to the spine).
    :param int group: Group sheets before cutting them.
        See help of command line --group option for more information.
    """
    if mark is None:
        mark = []

    if size is not None and signature is not None:
        raise ValueError(
            "Only one of `size` and `signature` arguments can be other than `None`."
        )
    if size is None and signature is None:
        size = DEFAULT_PAPER_SIZE
    if size is not None:
        # Convert size to signature
        if isinstance(size, str):
            size = tuple(float(dim) for dim in papersize.parse_papersize(size))
        files = pdf.Reader(files)
        sourcesize = files.size
        if bind in ("top", "bottom"):
            sourcesize = (2 * sourcesize[1], sourcesize[0])
        else:
            sourcesize = (2 * sourcesize[0], sourcesize[1])
        signature, omargin = size2signature(
            size,
            sourcesize=sourcesize,
            imargin=imargin,
            omargin=omargin,
        )

    CutStackFoldImpositor(
        imargin=imargin,
        omargin=omargin,
        mark=mark,
        last=last,
        signature=signature,
        bind=bind,
        creep=creep,
        group=group,
    ).impose(files, output)
