import re
from pathlib import Path
from typing import Any, Tuple, Union

from plumbum.cmd import hdiutil


def imageinfo(image_path: Union[str, Path], **kwargs: Any) -> str:
    """ Returns dmg file info"""
    return _run_hdiutil_command('imageinfo', image_path, **kwargs)


def attach(image_path: Union[str, Path], **kwargs: Any) -> Tuple:
    """ Attach dmg file to mount point"""
    output = _run_hdiutil_command('attach', image_path, **kwargs)
    if not output:
        raise ValueError("No output returned from hdiutil attach")
    res = re.findall(r'(/[a-zA-Z0-9\./]*\s?)', output)
    res = tuple(x.replace('\n', '') for x in res)
    return res


def detach(image_path: Union[str, Path], **kwargs: Any) -> str:
    """Detach mount point"""
    return _run_hdiutil_command('detach', image_path, **kwargs)


def create(image_path: Union[str, Path], **kwargs: Any) -> str:
    return _run_hdiutil_command('create', image_path, **kwargs)


def _run_hdiutil_command(command_name: str, image_path: str, **kwargs) -> str:
    """
    run hdiutil command. First argument is the `verb` and `**kwargs` are the `options`. `image_path` is
    mandatory.

    hdiutil Usage:
        Usage: hdiutil <verb> <options>
        <verb> is one of the following:
        help            	imageinfo
        attach          	isencrypted
        detach          	makehybrid
                    .....
    """
    command = [command_name, image_path]
    for k, v in kwargs.items():
        command.extend([f'-{k}', v])
    return hdiutil(command)
