import glob
import os
from typing import List

from ditidy import util
from ditidy.error import on_error

from . import clang_format
from . import dir_name
from . import extern_c
from . import file_name
from . import git_utils
from . import include_guard
from . import shellcheck

__all_files = {}


def __process_pattern_all(root_dir: str):
    """
    `root_dir`'in altındaki tüm dosyaları tarar
    ve eşleşen dosyaları döndürür.
    Pathler normalize edilir ve sıralanır.
    Eğer `root_dir` cache'te varsa cache döndürülür.

    Bu fonksiyonun esas amacı özellikle git check-ignore komutunun
    yavaşlığını gidermek.
    Program yaşamı boyunca geçerli olacak, `root_dir` altındaki kullanılabilir tüm dosyalar tek seferliğine belirleniyor
    ve daha sonra sonuçlar cacheleniyor.

    Bu fonksiyonu kullanacak fonksiyon ise kendi patterni ile bulduğu sonuçları bu fonksiyonun çıktısı ile kesiştirdiğinde
    kullanılabilecek pathleri bulacaktır.
    """
    root_dir = os.path.normpath(root_dir)
    if root_dir in __all_files:
        return __all_files.get(root_dir)

    paths = glob.glob("**/*", root_dir=root_dir, recursive=True, include_hidden=True)
    paths = [os.path.normpath(i) for i in paths]

    if git_utils.is_in_git_dir(root_dir):
        # hızlı olması için ilk önce git için exclude edilen dirlere eşit
        # veya için bulunan pathleri filtrele
        git_exclude_dirs = git_utils.get_exclude_dirs(root_dir)
        paths = [i for i in paths if not util.is_within_dir(i, git_exclude_dirs)]

        # kalan pathlerin hepsini tek tek git'in ignore edip etmediğini kontrol et
        ignored_paths = git_utils.get_ignored_paths(root_dir, paths)
        paths = list(set(paths)-set(ignored_paths))

    paths.sort()

    __all_files[root_dir] = paths
    return paths


def process_patterns(root_dir: str, patterns: list):
    """
    Patern listesine göre path'leri bulur, pathleri normalize eder ve sıralar.
    Tekrarlayan pathleri filtreler.
    Pathler file ve directory olabilir.

    Eğer patternlerden birisi herhangi bir path'e eşleşmiyorsa hata verir.
    """
    paths = []
    for pattern in patterns:
        temp = glob.glob(pattern, root_dir=root_dir, recursive=True, include_hidden=True)
        if len(temp) == 0:
            on_error(f"no path(s) found in the pattern= {pattern}")
        paths.extend(temp)
    paths = [os.path.normpath(i) for i in paths]
    paths = list(set(paths))

    # kullanılabilir tüm dosyalar ile bulunan pathlerin kesişimini al
    paths = list(set(paths) & set(__process_pattern_all(root_dir)))

    # son olarak sırala
    paths.sort()

    return paths


def __get_files(root_dir: str, includes: list, excludes: list):
    including_files = [i for i in process_patterns(root_dir, includes) if os.path.isfile(os.path.join(root_dir, i))]
    excluding_files = [i for i in process_patterns(root_dir, excludes) if os.path.isfile(os.path.join(root_dir, i))]

    files = list(set(including_files)-set(excluding_files))
    files.sort()
    return files


def get_files_wext(root_dir: str, includes: list, excludes: list, exts: List[str]):
    files = __get_files(root_dir, includes, excludes)
    files = [i for i in files if os.path.splitext(i)[1][1:] in exts]
    return files


def get_dirs(root_dir: str, includes: list, excludes: list):
    including_dirs = [i for i in process_patterns(root_dir, includes) if os.path.isdir(os.path.join(root_dir, i))]
    excluding_dirs = [i for i in process_patterns(root_dir, excludes) if os.path.isdir(os.path.join(root_dir, i))]

    dirs = list(set(including_dirs)-set(excluding_dirs))
    dirs.sort()

    return dirs


def checks(root_dir: str, config: dict):
    errors = {}

    options = config.get("options")
    checks = config.get("checks")
    for c in checks.keys():
        error = None
        if c == "dir-name":
            dirs = get_dirs(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"])
            error = dir_name.check(dirs)
        elif c == "file-name":
            files = __get_files(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"])
            error = file_name.check(root_dir, files)
        elif c == "include-guard":
            files = get_files_wext(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"], options["c_hdr_exts"]+options["cpp_hdr_exts"])
            error = include_guard.check(root_dir, files)
        elif c == "extern-c":
            files = get_files_wext(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"], options["c_hdr_exts"])
            error = extern_c.check(root_dir, files)
        elif c == "clang-format":
            files = get_files_wext(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"],
                                   options["c_hdr_exts"]+options["c_src_exts"]+options["cpp_hdr_exts"]+options["cpp_src_exts"])
            error = clang_format.check(root_dir, files)
        elif c == "shellcheck":
            files = get_files_wext(root_dir, checks.get(c)["includes"], checks.get(c)["excludes"], options["sh_exts"])
            error = shellcheck.check(root_dir, files)

        if error:
            errors[c] = error

    # print errors
    if errors:
        messages = []
        for i in errors:
            messages.append(f">>> {i}:{os.linesep}{os.linesep.join(errors[i])}")
        on_error(os.linesep+(os.linesep*2).join(messages))
