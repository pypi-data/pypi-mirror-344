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

"""Print pages, to be cut and folded, and eventually bound, to produce multiple books.

You want to print and bind several copies of a tiny A7 book.  Those books are made with A6 sheets (when you open the book, you get two A7 pages side-by-side, which is A6).  Since you can fit four A6 pages on an A4 page, this means that you can print four books at once.

To use this schema (without option --group):

- print your imposed file, two-sided;
- cut the stack of paper, to get several stacks (four in the example above);
- fold (once) and bind each stack of paper you got, separately;
- voilà! You now have several copies of your book.

With option --group=3 (for instance), repeat the step above for every group of three sheets. You get several signatures, that you have to bind together to get a proper book.
"""  # pylint: disable=line-too-long

import dataclasses
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
    Matrix,
    Page,
    cutstackfold,
    nocreep,
    pdf,
    size2signature,
)


@dataclasses.dataclass
class CopyCutFoldImpositor(cutstackfold.CutStackFoldImpositor):
    """Perform imposition of source files, with the 'copycutfold' schema."""

    def blank_page_number(self, source):
        if source % 4 == 0:
            return 0
        return 4 - (source % 4)

    def base_matrix(self, total):
        """Yield the first matrix.

        This matrix contains the arrangement of source pages on the output pages.

        :param int total: Total number of source pages.
        """

        recto, verso = (
            [
                [None for _ in range(self.signature[1])]
                for _ in range(2 * self.signature[0])
            ]
            for _ in range(2)
        )

        for x, y in itertools.product(*map(range, self.signature)):
            recto[2 * x][y] = Page(3, **self.margins(2 * x, y))
            recto[2 * x + 1][y] = Page(0, **self.margins(2 * x + 1, y))
            verso[2 * x][y] = Page(1, **self.margins(2 * x, y))
            verso[2 * x + 1][y] = Page(2, **self.margins(2 * x + 1, y))

        yield Matrix(recto, rotate=BIND2ANGLE[self.bind])
        yield Matrix(verso, rotate=BIND2ANGLE[self.bind])

    def matrixes(self, pages: int):
        assert pages % 4 == 0

        if self.group == 0:
            group = math.ceil(pages / 4)
        else:
            group = self.group

        # First, we compute the first group of pages
        base_matrixes = list(self.base_matrix(4 * group))
        group_matrixes = []
        for i in range(group):
            group_matrixes.extend(
                self.insert_sheets(
                    (matrix.copy() for matrix in base_matrixes), i, 4 * group, 2
                )
            )

        # Then, we repeat the group as many times as necessary
        for i in range(math.ceil(pages / (4 * group))):
            for matrix in group_matrixes:
                yield matrix.stack(i * 4 * group)


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
    """Perform imposition of source files into an output file, using the copy-cut-fold schema.

    :param Sequence[str|pathlib.Path|io.BytesIO] files: List of source files (as filenames (strings or :class:`pathlib.Path`), or :class:`io.BytesIO` streams).
    :param str | pathlib.Path | io.BytesIO output: Output file.
    :param float|numbers.Real|decimal.Decimal|Margins omargin: Output margin. It can be:
        a :class:`numbers.Real` or :class:`decimal.Decimal`` (unit is pt),
        a :class:`Margins` object,
        a :class:`str`, to be parsed by :func:`papersize.parse_length`.
    :param float|numbers.Real|decimal.Decimal imargin: Input margin. Same types and meaning as `omargin` (excepted that :class:`Margins` objects is not accepted).
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
        and return the space to be left between two adjacent pages.
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

    CopyCutFoldImpositor(
        imargin=imargin,
        omargin=omargin,
        mark=mark,
        last=last,
        signature=signature,
        bind=bind,
        creep=creep,
        group=group,
    ).impose(files, output)
