import os
from pathlib import Path
from tempfile import TemporaryDirectory

from plumbum.cmd import cp
from plumbum.cmd import open as open_finder
from plumbum.cmd import sudo

from pybinpack import hdiutil


class BinpackFS:
    @classmethod
    def create_from_binpack_dmg(cls, binpack_file: Path) -> 'BinpackFS':
        """ Create a BinpackFS instance from a given binpack.dmg file """
        _, mountpoint = hdiutil.attach(binpack_file)
        if not mountpoint:
            raise FileNotFoundError(mountpoint)

        tmp_fs = Path(TemporaryDirectory().name)
        cls._copy_and_change_permissions(mountpoint, tmp_fs)
        hdiutil.detach(mountpoint)

        return BinpackFS(tmp_fs)

    @classmethod
    def create_from_fs(cls, fs: Path) -> 'BinpackFS':
        """ Create a BinpackFS instance from a given FS path """
        tmp_fs = Path(TemporaryDirectory().name)
        cls._copy_and_change_permissions(fs, tmp_fs)

        return BinpackFS(tmp_fs)

    def __init__(self, path: Path):
        self.path = path

    def open_in_finder(self) -> None:
        open_finder(self.path)

    def pack(self, out_file: Path, override: bool = False, size: str = '20m') -> None:
        """
        Creates new image file from the temp directory.
        """
        if override and out_file.exists():
            out_file.unlink()

        hdiutil.create(out_file,
                       size=size,
                       layout='NONE',
                       format='ULFO',
                       srcdir=self.path,
                       fs='HFS+')

    def __enter__(self) -> 'BinpackFS':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        """
        Delete the temp dir and detach the image.
        """
        sudo('rm', '-rf', self.path)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} PATH:{self.path}>'

    @staticmethod
    def _copy_and_change_permissions(src: Path, dst: Path):
        cp('-a', '-R', str(src) + os.sep, dst)
        sudo('chown', '-R', '0:0', dst)
