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

"""A one-page fanzine, with a poster on the back.

On this schema, you get an 8 pages book which, once unfolded, gives a poster on the back
(see `some photos
<http://experimentwithnature.com/03-found/experiment-with-paper-how-to-make-a-one-page-zine/>`__).

This command only perform imposition of the front of your fanzine.
It is your job to print the poster on the back.
"""

import dataclasses
import io
import numbers
import pathlib
from collections.abc import Sequence

from .. import BIND2ANGLE, AbstractImpositor, Matrix, Page


@dataclasses.dataclass
class OnePageZineImpositor(AbstractImpositor):
    """Perform imposition of source files, with the 'one-page-zine' schema.

    See
    `http://experimentwithnature.com/03-found/experiment-with-paper-how-to-make-a-one-page-zine/`.
    """

    bind: str = "left"

    def blank_page_number(self, source):
        if source % 8 == 0:
            return 0
        return 8 - (source % 8)

    def base_matrix(self, total):
        """Yield a single matrix.

        This matrix contains the arrangement of source pages on the output pages.
        """
        # pylint: disable=unused-argument
        yield Matrix(
            [
                [
                    Page(4, rotate=180, top=self.omargin.top, left=self.omargin.left),
                    Page(5, bottom=self.omargin.bottom, left=self.omargin.left),
                ],
                [
                    Page(3, rotate=180, top=self.omargin.top),
                    Page(6, bottom=self.omargin.bottom),
                ],
                [
                    Page(2, rotate=180, top=self.omargin.top),
                    Page(7, bottom=self.omargin.bottom),
                ],
                [
                    Page(1, rotate=180, top=self.omargin.top, right=self.omargin.right),
                    Page(0, bottom=self.omargin.bottom, right=self.omargin.right),
                ],
            ],
            rotate=BIND2ANGLE[self.bind],
        )

    def matrixes(self, pages: int):
        assert pages % 8 == 0
        yield from self.stack_matrixes(
            list(self.base_matrix(pages)),
            step=8,
            repeat=pages // 8,
        )

    def crop_marks(self, *, number, total, matrix, outputsize, inputsize):
        # pylint: disable=too-many-arguments
        left, right, top, bottom = self._crop_space()

        yield ((0, self.omargin.top), (self.omargin.left - left, self.omargin.top))
        yield ((self.omargin.left, 0), (self.omargin.left, self.omargin.top - top))
        yield (
            (outputsize[0], self.omargin.top),
            (outputsize[0] - self.omargin.right + right, self.omargin.top),
        )
        yield (
            (outputsize[0] - self.omargin.right, 0),
            (outputsize[0] - self.omargin.right, self.omargin.top - top),
        )
        yield (
            (0, outputsize[1] - self.omargin.top),
            (self.omargin.left - left, outputsize[1] - self.omargin.top),
        )
        yield (
            (self.omargin.left, outputsize[1]),
            (self.omargin.left, outputsize[1] - self.omargin.bottom + bottom),
        )
        yield (
            (outputsize[0], outputsize[1] - self.omargin.bottom),
            (
                outputsize[0] - self.omargin.right + right,
                outputsize[1] - self.omargin.bottom,
            ),
        )
        yield (
            (outputsize[0] - self.omargin.right, outputsize[1]),
            (
                outputsize[0] - self.omargin.right,
                outputsize[1] - self.omargin.bottom + bottom,
            ),
        )


def impose(
    files: Sequence[str | pathlib.Path | io.BytesIO],
    output: str | pathlib.Path | io.BytesIO,
    *,
    omargin=0,
    last=0,
    mark=None,
    bind="left",
):
    # pylint: disable=too-many-arguments
    """Perform imposition of source files into an output file, to be printed as a "one page zine".

    :param Sequence[str|pathlib.Path|io.BytesIO] files: List of source files
        (as filenames (strings or :class:`pathlib.Path`), or :class:`io.BytesIO` streams).
    :param str | pathlib.Path | io.BytesIO output: Output file.
    :param number.Real|Margins|decimal.Decimal|str omargin: Output margin, as:
        a number :class:`number.Real` or :class:`decimal.Decimal`,
        a :class:`Margins` object,
        or a :class:`str`, that is to be parsed by :func:`papersize.parse_length`.
    :param int last: Number of last pages (of the source files) to keep at the
        end of the output document.  If blank pages were to be added to the
        source files, they would be added before those last pages.
    :param list[str] mark: List of marks to add.
        Only crop marks are supported (`mark=['crop']`); everything else is silently ignored.
    :param str bind: Binding edge. Can be one of `left`, `right`, `top`, `bottom`.

    See
    `http://experimentwithnature.com/03-found/experiment-with-paper-how-to-make-a-one-page-zine/`.
    """
    if mark is None:
        mark = []

    OnePageZineImpositor(
        omargin=omargin,
        last=last,
        mark=mark,
        bind=bind,
    ).impose(files, output)
