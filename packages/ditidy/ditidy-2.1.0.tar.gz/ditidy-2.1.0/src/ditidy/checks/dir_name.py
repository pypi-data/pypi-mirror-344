import os
import re

DIR_NAME_PATTERN = r'^[a-z0-9]+(_[a-z0-9]+)*$'

EXCLUDED_DIRS = [".vscode"]


def check(dirs: list):
    dirs = [i for i in dirs if i not in EXCLUDED_DIRS]
    fails = []
    for d in dirs:
        dir = os.path.basename(d)
        if re.match(DIR_NAME_PATTERN, dir) is None:
            fails.append(d)
    if len(fails) > 0:
        return fails
    return None
