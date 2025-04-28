# Copyright 2024 Louis Paternault
#
# This file is part of pdfimpose-web.
#
# Pdfimpose-web is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pdfimpose-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfimpose-web. If not, see <https://www.gnu.org/licenses/>.

"""Resize PDF

This is a test program. It may contain bugs and change without notice. Do not use it.

However, this could be easily be turned into a proper package.
If you think this might be useful, send me an email, it should not take me that long…
"""

import sys
import textwrap

from . import resize_scale, resize_size

USAGE = textwrap.dedent(
    # pylint: disable=line-too-long
    """\
        pdfresize: Resize a PDF file (for instance, turn a A4 file into a A5 file).

        pdfresize [--help] [-h]
            Print Help and exit

        pdfresize [--version]
            Print version and exit

        pdfresize xSCALE SOURCE DEST
            Multiply width and height of SOURCE by SCALE, and save resulting file in DEST.

        pdfresize /SCALE SOURCE DEST
            Divide width and height of SOURCE by SCALE, and save resulting file in DEST.

        pdfresize SIZE SOURCE DEST
            Scale SOURCE file to fit SIZE, and save resulting file in DEST.
            SIZE can be a named paper format (e.g. "A4" or "letter"), or dimentions (e.g. "21cmx297mm" or "1inx2in").
        """
)


def main():
    """Main function: parse arguments, and run script."""
    print(
        # pylint: disable=line-too-long
        "This script is experimental. Use it as long as you want, but it may change, be renamed, disapear without notice. If you think it deserves some polishing and its own package, give me a word about it.",
        file=sys.stderr,
    )
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print(USAGE)
        sys.exit(0)
    if len(sys.argv) == 2 and sys.argv[1] == "--version":
        print("This is experimental. It does not have any version number yet…")
        sys.exit(0)
    if len(sys.argv) != 4:
        print(USAGE)
        sys.exit(1)
    size, source, dest = sys.argv[1:]
    if size.startswith("x"):
        resize_scale(source, dest, float(size[1:]))
    elif size.startswith("/"):
        resize_scale(source, dest, 1 / float(size[1:]))
    else:
        resize_size(source, dest, size)


if __name__ == "__main__":
    main()
