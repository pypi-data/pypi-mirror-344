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

"""Parse arguments for the schema "copycutfold"."""

import io
import logging
import sys

from ... import UserError
from .. import ArgumentParser
from . import __doc__ as DESCRIPTION
from . import impose


def main(argv=None):
    """Main function"""

    parser = ArgumentParser(
        subcommand="copycutfold",
        description=DESCRIPTION,
        options=[
            "omargin",
            "imargin",
            "mark",
            "last",
            "cutsignature",
            "format",
            "bind",
            "creep",
            "group0",
        ],
    )

    try:
        args = parser.parse_args(argv)
        impose(**vars(args))
        if isinstance(args.output, io.BytesIO):
            sys.stdout.buffer.write(args.output.getvalue())

    except UserError as uerror:
        logging.error(uerror)
        sys.exit(1)


if __name__ == "__main__":
    main()
