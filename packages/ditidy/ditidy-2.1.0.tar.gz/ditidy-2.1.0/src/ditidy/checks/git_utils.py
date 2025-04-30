import multiprocessing
import os
import subprocess
import sys
from pathlib import Path
from typing import List

from ditidy import util
from ditidy.error import on_error


def is_in_git_dir(root_dir: str):
    """
    bulunduğu dizinin bir git reposu olup olmadığını kontrol eder
    """
    result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=root_dir, capture_output=True, text=True)
    if result.returncode == 128:
        return False
    elif result.returncode == 0:
        return True
    else:
        sys.stderr.write(result.stderr)
        on_error("failed")


def __get_git_repo_root(root_dir: str):
    """
    git reposunun bulunduğu dizinin mutlak pathini döner
    """
    result = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=root_dir, capture_output=True, text=True)
    if result.returncode == 0:
        return os.path.dirname(result.stdout)
    else:
        sys.stderr.write(result.stderr)
        on_error("failed")


def __get_submodule_dirs(root_dir: str):
    """
    gitteki submodule'lerin dizinlerini root_dir`'e göre listeler, normalize eder ve sıralar
    """
    repo_root = __get_git_repo_root(root_dir)
    output = subprocess.check_output(f"git config --file {repo_root}/.gitmodules --get-regexp path | awk '{{print $2}}'", cwd=root_dir, shell=True, text=True)
    if len(output) == 0:
        return []
    dirs = output.splitlines()

    # sadece bulunan dizindeki modülleri kullan
    dirs = [i for i in dirs if Path(os.path.join(repo_root, i)).is_relative_to(Path(root_dir))]
    # modülleri bulunan dizine göre temsil et
    dirs = [Path(os.path.join(repo_root, i)).relative_to(Path(root_dir)) for i in dirs]

    dirs = [os.path.normpath(i) for i in dirs]
    dirs.sort()
    return dirs


def __get_ignored_dirs_internal(root_dir: str, excludes: List[str], curr_dir: str):
    """
    `root_dir`'de recursive olarak git tarafından ignore edilen tüm dizinleri listeler
    """
    curr_abs_dir = os.path.join(root_dir, curr_dir)
    all_dirs = [i for i in os.listdir(curr_abs_dir) if os.path.isdir(os.path.join(curr_abs_dir, i))]
    all_dirs = [i for i in all_dirs if not util.is_within_dir(os.path.join(curr_abs_dir, i), [os.path.join(root_dir, i) for i in excludes])]

    ig_dirs = []
    if len(all_dirs) > 0:
        ignored_dirs = get_ignored_paths(curr_abs_dir, all_dirs)
        ig_dirs.extend(ignored_dirs)
        not_ignored_dirs = list(set(all_dirs)-set(ignored_dirs))
        for dir in not_ignored_dirs:
            child_dirs = __get_ignored_dirs_internal(root_dir, excludes, os.path.join(curr_dir, dir))
            ig_dirs.extend([os.path.join(dir, j) for j in child_dirs])

    return ig_dirs


def __get_ignored_dirs(root_dir: str, excludes: List[str]):
    """
    `root_dir`'de recursive olarak git tarafından ignore edilen tüm dizinleri listeler, normalize eder ve sıralar
    """
    ig_dirs = __get_ignored_dirs_internal(root_dir, excludes, ".")
    ig_dirs = [os.path.normpath(i) for i in ig_dirs]
    ig_dirs.sort()
    return ig_dirs


def get_exclude_dirs(root_dir: str):
    """
    `root_dir`'e göre .git, submodule ve ignore edilen dizinleri listeler, normalize eder ve sıralar
    """
    exclude_dirs = [".git"]
    exclude_dirs.extend(__get_submodule_dirs(root_dir))
    exclude_dirs.extend(__get_ignored_dirs(root_dir, exclude_dirs))

    exclude_dirs = [os.path.normpath(i) for i in exclude_dirs]
    exclude_dirs = list(set(exclude_dirs))
    exclude_dirs.sort()
    return exclude_dirs


def __get_ignored_paths_worker(root_dir, paths):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "scripts", "git_check_ignore.sh")
    return subprocess.check_output([script]+paths, cwd=root_dir, text=True)


def get_ignored_paths(root_dir: str, paths: List[str]):
    pool_args = [(root_dir, i) for i in util.chunks_for_count(paths, multiprocessing.cpu_count())]
    results = util.pool_wrapper(__get_ignored_paths_worker, pool_args)
    results = "".join(results)
    results = [int(i) for i in results.splitlines()]
    return [path for index, path in enumerate(paths) if results[index] == 0]
