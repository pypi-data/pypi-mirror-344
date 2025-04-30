import difflib
import os
import subprocess
import sys

from ditidy import util


def colorize(diff_lines):
    def bold(s):
        return '\x1b[1m' + s + '\x1b[0m'

    def cyan(s):
        return '\x1b[36m' + s + '\x1b[0m'

    def green(s):
        return '\x1b[32m' + s + '\x1b[0m'

    def red(s):
        return '\x1b[31m' + s + '\x1b[0m'

    for line in diff_lines:
        if line[:4] in ['--- ', '+++ ']:
            yield bold(line)
        elif line.startswith('@@ '):
            yield cyan(line)
        elif line.startswith('+'):
            yield green(line)
        elif line.startswith('-'):
            yield red(line)
        else:
            yield line


def make_diff(file, original, reformatted):
    return list(
        difflib.unified_diff(
            original,
            reformatted,
            fromfile='{}\t(original)'.format(file),
            tofile='{}\t(reformatted)'.format(file),
            n=3))


def print_diff(diff_lines, use_color):
    if use_color:
        diff_lines = colorize(diff_lines)
    sys.stdout.writelines(diff_lines)


def __formatted_worker(root_dir: str, file: str):
    file_abs = os.path.join(root_dir, file)
    proc = subprocess.Popen(['clang-format', "--fail-on-incomplete-format", file_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    outs = list(proc.stdout.readlines())
    errs = list(proc.stderr.readlines())
    proc.wait()
    if proc.returncode:
        raise Exception("".join(errs))

    with open(file_abs, "r") as f:
        orig_content = f.readlines()
    formatted_content = outs
    return (file, make_diff(file, orig_content, formatted_content))


def check(root_dir: str, files: list):
    if len(files) == 0:
        return None

    pool_args = [(root_dir, i) for i in files]
    results = util.pool_wrapper(__formatted_worker, pool_args)
    fails = [i for i in results if i[1]]

    for i in fails:
        print_diff(i[1], True)

    if fails:
        return [i[0] for i in fails]
    return None
