from pathlib import Path

import click

from pybinpack.binpack import BinpackFS

SHELL_USAGE = f"""Welcome to PyBinpack interactive shell! 🐍
Use the {click.style(fg='cyan', bold=True, text='bp')} global in order to manipulate the given binpack file."""


@click.group()
def cli():
    pass


@cli.command()
@click.argument('binpack_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def modify(binpack_file: str):
    binpack_file = Path(binpack_file)
    with BinpackFS.create_from_binpack_dmg(binpack_file) as bp:
        print(f'Extracted FS can be found at: {bp.path}')
        input('HIT RETURN WHEN DONE MODIFYING> ')
        bp.pack(binpack_file, override=True)


@cli.command()
@click.argument('binpack_file', type=click.Path(exists=False, file_okay=True, dir_okay=False))
@click.argument('fs', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--override', is_flag=True)
def create(binpack_file: str, fs: str, override: bool):
    fs = Path(fs)
    binpack_file = Path(binpack_file)
    with BinpackFS.create_from_fs(fs) as bp:
        bp.pack(binpack_file, override=override)


if __name__ == '__main__':
    cli()
