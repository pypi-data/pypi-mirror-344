import os
import subprocess
import sys

from ditidy import util


def __formatted_worker(root_dir: str, file: str):
    result = subprocess.run(["shellcheck", os.path.join(root_dir, file)], capture_output=True, text=True)
    if result.returncode == 0:
        return (file, None)
    return (file, result.stdout)


def check(root_dir: str, files: list):
    if len(files) == 0:
        return None

    pool_args = [(root_dir, i) for i in files]
    results = util.pool_wrapper(__formatted_worker, pool_args)
    fails = [i for i in results if i[1]]

    for i in fails:
        sys.stderr.write(i[1])

    if fails:
        return [i[0] for i in fails]
    return None
