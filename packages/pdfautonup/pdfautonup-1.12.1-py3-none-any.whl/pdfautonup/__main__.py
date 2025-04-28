#!/usr/bin/env python3

# Copyright Louis Paternault 2014-2025
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Main function for the command."""

import io
import logging
import os
import sys

from . import errors, options, pdfautonup, pdfbackend

LOGGER = logging.getLogger("pdfautonup")


def _progress_printer(string):
    """Returns a function that prints the progress message."""

    def print_progress(page, total):
        """Print progress message."""
        try:
            text = string.format(
                page=page, total=total, percent=int(page * 100 / total)
            )
        except:  # pylint: disable=bare-except
            text = string
        print(text, end="")
        sys.stdout.flush()

    return print_progress


def _process_output(file, output):
    if output == "-" or (output is None and not isinstance(file, str)):
        return io.BytesIO()
    if output is None:
        if file.endswith(".pdf"):
            return f"""{file[: -len(".pdf")]}-nup.pdf"""
        return f"{file}-nup.pdf"
    raise TypeError()


def main():
    """Main function"""
    try:
        arguments = options.commandline_parser().parse_args(sys.argv[1:])

        if arguments.verbose:
            # pylint: disable=no-member
            sys.stderr.write(f"Using pdf backend {pdfbackend.get_backend().VERSION}\n")

        # Process input file names
        if None in arguments.files and arguments.interactive:
            LOGGER.error(
                """Cannot ask user input while reading files from standard input. """
                """Try removing the "--interactive" (or "-i") option."""
            )
            sys.exit(1)
        for i, file in enumerate(arguments.files):
            if file is None:
                arguments.files[i] = io.BytesIO(sys.stdin.buffer.read())

        # Compute output file name
        output = _process_output(arguments.files[0], arguments.output)
        if isinstance(output, str) and arguments.interactive and os.path.exists(output):
            if (
                input(f"File {output} already exists. Overwrite (y/[n])? ").lower()
                != "y"
            ):
                raise errors.PdfautonupError("Cancelled by user.")

        pdfautonup(
            arguments.files,
            output,
            arguments.target_size,
            algorithm=arguments.algorithm,
            repeat=arguments.repeat,
            orientation=arguments.orientation,
            progress=_progress_printer(arguments.progress),
            more={
                "gap": arguments.gap,
                "margin": arguments.margin,
            },
        )
        if not (arguments.progress.endswith("\n") or arguments.progress == ""):
            print()
        if isinstance(output, io.BytesIO):
            sys.stdout.buffer.write(output.getvalue())
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except errors.PdfautonupError as error:
        LOGGER.error(error)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
