# Copyright 2025 Louis Paternault
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

"""Test pdfimpose, as a library"""

import decimal
import functools
import io
import pathlib
import sys
import tempfile
import unittest

from pdfimposeweb import pdfresize

from .. import TestComparePDF

TEST_DATA_DIR = pathlib.Path(__file__).parent / "data"


class TestPDFResize(TestComparePDF):
    """Test library calls"""

    @staticmethod
    def controlname(name):
        """Return the name of the control file corresponding to `name`.

        >>> TestPDFResize().controlname("/foo/bar/baz.pdf")
        '/foo/bar/baz-control.pdf'
        """
        return name.parent / f"{name.stem}-control{name.suffix}"

    def test_resize_size(self):
        """Test function pdfresize.resize_size."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-resized-a5.pdf"
        pdfresize.resize_size(sourcename, destname, size="A5")
        self.assertPdfEqual(destname, self.controlname(destname))

    def test_resize_scale(self):
        """Test function pdfresize.resize_scale."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-scaled-x2.pdf"
        pdfresize.resize_scale(sourcename, destname, scale=2)
        self.assertPdfEqual(destname, self.controlname(destname))


class TestFileFormats(TestPDFResize):
    """Test that several file formats are accepted as input and output files."""

    def test_bytesio_scale(self):
        """Test that io.BytesIO is a correct file format."""
        # Set up files
        with open(TEST_DATA_DIR / "a6.pdf", mode="br") as sourcefile:
            sourceio = io.BytesIO(sourcefile.read())
        destio = io.BytesIO()

        # Perform resizing
        pdfresize.resize_scale(sourceio, destio, scale=2)

        # Compare files
        with tempfile.NamedTemporaryFile() as destfile:
            destfile.write(destio.getvalue())
            destfile.flush()
            self.assertPdfEqual(
                destfile.name, self.controlname(TEST_DATA_DIR / "a6-scaled-x2.pdf")
            )

    def test_bytesio_size(self):
        """Test that io.BytesIO is a correct file format."""
        # Set up files
        with open(TEST_DATA_DIR / "a6.pdf", mode="br") as sourcefile:
            sourceio = io.BytesIO(sourcefile.read())
        destio = io.BytesIO()

        # Perform resizing
        pdfresize.resize_size(sourceio, destio, size="A5")
        # Compare files
        with tempfile.NamedTemporaryFile() as destfile:
            destfile.write(destio.getvalue())
            destfile.flush()
            self.assertPdfEqual(
                destfile.name, self.controlname(TEST_DATA_DIR / "a6-resized-a5.pdf")
            )

    def test_str_size(self):
        """Test that str is a correct file format."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-resized-a5.pdf"
        pdfresize.resize_size(str(sourcename), str(destname), size="A5")
        self.assertPdfEqual(destname, self.controlname(destname))

    def test_pathlib_size(self):
        """Test that pathlib.Path is a correct file format."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-resized-a5.pdf"
        pdfresize.resize_size(
            pathlib.Path(sourcename), pathlib.Path(destname), size="A5"
        )
        self.assertPdfEqual(destname, self.controlname(destname))

    def test_pathlib_scale(self):
        """Test that pathlib.Path is a correct file format."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-scaled-x2.pdf"
        pdfresize.resize_scale(
            pathlib.Path(sourcename), pathlib.Path(destname), scale=2
        )
        self.assertPdfEqual(destname, self.controlname(destname))

    def test_str_scale(self):
        """Test that str is a correct file format."""
        sourcename = TEST_DATA_DIR / "a6.pdf"
        destname = TEST_DATA_DIR / "a6-scaled-x2.pdf"
        pdfresize.resize_scale(str(sourcename), str(destname), scale=2)
        self.assertPdfEqual(destname, self.controlname(destname))
