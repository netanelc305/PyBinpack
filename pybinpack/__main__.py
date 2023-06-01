from pathlib import Path

import click
import IPython

from pybinpack.binpack import ExtractedBinpack

SHELL_USAGE = f"""Welcome to PyBinpack interactive shell! 🐍
Use the {click.style(fg='cyan', bold=True, text='bp')} global in order to manipulate the given binpack file."""


@click.command()
@click.argument('binpack_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def cli(binpack_file: str):
    IPython.embed(
        header=SHELL_USAGE,
        user_ns={
            'bp': ExtractedBinpack.create_extracted_binpack(Path(binpack_file)),
        })


if __name__ == '__main__':
    cli()
