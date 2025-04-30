import os
import re


from . import git_utils
from .dir_name import DIR_NAME_PATTERN


FILE_NAME_PATTERN = DIR_NAME_PATTERN


def __get_excluded_files(root_dir: str):
    ex = []
    if git_utils.is_in_git_dir(root_dir):
        ex.extend([".gitignore", ".gitmodules"])
    return ex


def check(root_dir: str, files: list):
    files = [i for i in files if os.path.basename(i) not in __get_excluded_files(root_dir)]
    fails = []
    for f in files:
        dir = os.path.splitext(os.path.basename(f))[0]
        if re.match(FILE_NAME_PATTERN, dir) is None:
            fails.append(f)
    if len(fails) > 0:
        return fails
    return None
