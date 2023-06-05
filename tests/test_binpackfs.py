from pathlib import Path

from pybinpack.binpack import BinpackFS

FILENAME = 'file'
CONTENTS = b'abc'


def test_create_and_modify(tmp_path: Path):
    binpack_dmg = tmp_path / 'binpack.dmg'
    (tmp_path / FILENAME).write_bytes(CONTENTS)
    with BinpackFS.create_from_fs(tmp_path) as bp:
        bp.pack(binpack_dmg)

    with BinpackFS.create_from_binpack_dmg(binpack_dmg) as bp2:
        assert (bp2.path / FILENAME).read_bytes() == CONTENTS
