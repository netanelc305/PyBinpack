import os
from pathlib import Path
from tempfile import TemporaryDirectory

from plumbum.cmd import cp
from plumbum.cmd import open as open_finder
from plumbum.cmd import sudo

import hdiutil


class ExtractedBinpack:
    @staticmethod
    def create_extracted_binpack(binpack_file: Path, extracted_binpack: Path = None, override: bool = False,
                                 open_in_finder: bool = False, cleanup: bool = True) -> 'ExtractedBinpack':
        """
        Extract the input image into temp dir.
        """
        _, mountpoint = hdiutil.attach(binpack_file)
        if not mountpoint:
            raise FileNotFoundError(mountpoint)

        if not extracted_binpack:
            extracted_binpack = TemporaryDirectory().name
        else:
            if override:
                sudo('rm', '-rf', extracted_binpack)
            else:
                raise FileExistsError(extracted_binpack)

        cp('-a', '-R', mountpoint + os.sep, extracted_binpack)
        hdiutil.detach(mountpoint)

        if open_in_finder:
            open_finder(extracted_binpack)

        return ExtractedBinpack(Path(extracted_binpack), cleanup=cleanup)

    def __init__(self, extracted_binpack: Path, cleanup: bool):
        self.extracted_binpack = extracted_binpack
        self._cleanup = cleanup

    def pack(self, out_file: str, override: bool = False, size: str = '20m') -> None:
        """
        Creates new image file from the temp directory.
        """
        out_file = Path(out_file)
        if override and out_file.exists():
            out_file.unlink()
        sudo('chown', '-R', '0:0', self.extracted_binpack)

        hdiutil.create(out_file,
                       size=size,
                       layout='NONE',
                       format='ULFO',
                       srcdir=self.extracted_binpack,
                       fs='HFS+')

    def __enter__(self) -> 'ExtractedBinpack':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.pack()
        if self._cleanup:
            self.cleanup()

    def cleanup(self) -> None:
        """
        Delete the temp dir and detach the image.
        """
        sudo('rm', '-rf', self.extracted_binpack)

    def __repr__(self):
        return f'<{self.__class__.__name__} PATH:{self.extracted_binpack},CLEANUP:{self._cleanup}>'
