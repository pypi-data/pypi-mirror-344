import os
from typing import List

from ditidy.error import on_error

import yaml
import yaml.scanner

CHECKS = ["dir-name", "file-name", "include-guard", "extern-c", "clang-format", "shellcheck"]

DEFAULT_C_HDR_EXTS = ["h"]
DEFAULT_C_SRC_EXTS = ["c"]

DEFAULT_CPP_HDR_EXTS = ["h", "hh"]
DEFAULT_CPP_SRC_EXTS = ["cpp", "cc", "ino"]

DEFAULT_SH_EXTS = ["sh"]


def load_options(config):
    options = {}

    if "options" not in config:
        config["options"] = {}

    content = config.get("options")
    if not isinstance(content, dict):
        on_error("options: should be dictionary")

    options["includes"] = load_single_or_array_str("includes", content, ["**/*"])
    options["excludes"] = load_single_or_array_str("excludes", content, [])

    options["c_hdr_exts"] = load_single_or_array_str("c_hdr_exts", content, DEFAULT_C_HDR_EXTS)
    options["c_src_exts"] = load_single_or_array_str("c_src_exts", content, DEFAULT_C_SRC_EXTS)

    options["cpp_hdr_exts"] = load_single_or_array_str("cpp_hdr_exts", content, DEFAULT_CPP_HDR_EXTS)
    options["cpp_src_exts"] = load_single_or_array_str("cpp_src_exts", content, DEFAULT_CPP_SRC_EXTS)

    options["sh_exts"] = load_single_or_array_str("sh_exts", content, DEFAULT_SH_EXTS)

    for key in content:
        on_error(f"{key}: unknown key in the options")

    del config["options"]
    return options


def update_check_list(check_list: List[str], new_list: List[str], add: bool):
    for item in new_list:
        if item in check_list:
            check_list.remove(item)
    if add:
        check_list.extend(new_list)


def load_check_list(checks: any):
    check_list = []
    if not isinstance(checks, list):
        on_error("checks field should be list")
    for check_item in checks:
        if not isinstance(check_item, str):
            on_error(f"{check_item} field should be string")
        add = True
        if check_item.startswith("-"):
            add = False
        check = check_item.lstrip("-")
        if check == "*":
            update_check_list(check_list, CHECKS, add)
        elif check in CHECKS:
            update_check_list(check_list, [check], add)
        else:
            on_error(f"unknown check= {check}")
    return check_list


def load_single_or_array_str(key: str, data: any, default: List[str]):
    """
    `key`'i `data` içinde kontrol eder. String veya string listesi olmalıdır.

    `key`'in değeri boş olamaz.

    Eğer `key` yoksa, `default` değer atanır.

    `default` boş olabilir.
    """
    if key in data:
        content = data.get(key)
        if isinstance(content, str):
            content = [content]
        elif isinstance(content, list) and len(content) > 0:
            for i in content:
                if not isinstance(i, str):
                    on_error(f"{key}: should be string or array of string")
        else:
            on_error(f"{key}: should be string or array of string")
        del data[key]
        return content
    return default


def load_check_option(key: any, content: any, options: dict):
    if key not in CHECKS:
        on_error(f"unknown check option key= {key}")
    elif not isinstance(content, dict):
        on_error(f"{key}: should be dictionary")

    check_options = {}
    check_options["includes"] = load_single_or_array_str("includes", content, options["includes"])
    check_options["excludes"] = options["excludes"] + load_single_or_array_str("excludes", content, [])

    for sub_key in content:
        on_error(f"unknown key in the check option {key}= {sub_key}")

    return check_options


def load_check_options(data: any, options: dict):
    if "check-options" not in data:
        data["check-options"] = {}

    content = data["check-options"]

    if not isinstance(content, dict):
        on_error("check-options: should be dictionary")

    check_options = {}
    for key in content.keys():
        option = load_check_option(key, content.get(key), options)
        option["exist"] = True
        check_options[key] = option
    del data["check-options"]

    # belirtilmeyen check optionların default değerlerini yükle
    missing_check_options = list(set(CHECKS)-set(check_options.keys()))
    for i in missing_check_options:
        option = load_check_option(i, {}, options)
        option["exist"] = False
        check_options[i] = option

    return check_options


def load(data: any):
    if not isinstance(data, dict):
        on_error("invalid config format")

    options = load_options(data)

    check_list = load_check_list(data.get("checks"))
    del data["checks"]

    all_checks = load_check_options(data, options)

    for key in data:
        on_error(f"{key}: unknown key in the config file")

    exclusive_checks = {k: v for k, v in all_checks.items() if v["exist"]}
    missing_checks = list(set(exclusive_checks.keys())-set(check_list))
    if len(missing_checks) > 0:
        on_error(f"missing check(s)= {', '.join(missing_checks)}")

    enabled_checks = {k: v for k, v in all_checks.items() if k in check_list}
    return {"options": options, "checks": enabled_checks}


def parse(file: str):
    if not os.path.exists(file) or not os.path.isfile(file):
        on_error("config file could not found")

    with open(file, "r") as config_file:
        try:
            data = yaml.safe_load(config_file)
        except yaml.scanner.ScannerError:
            on_error("invalid document format")
        return load(data)
