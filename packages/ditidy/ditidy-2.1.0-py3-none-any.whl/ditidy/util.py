import multiprocessing
from pathlib import Path
from typing import List


def is_within_dir(p: str, dirs: List[str]):
    """
    `p` yolunun `dirs` veya `dirs`'in içinde olup olmadığını kontrol eder
    """
    pp = Path(p)

    for d in dirs:
        if pp == Path(d) or Path(d) in pp.parents:
            return True
    return False


def chunks_for_count(data: list, count: int):
    """
    `l` listesini maksimum `count` adet kadar parçaya mümkün olan en eşit şekilde ardışık olarak ayırır.
    """
    chunk_lens = [[] for _ in range(count)]
    for i, val in enumerate(data):
        chunk_lens[i % count].append(val)
    chunk_lens = [len(i) for i in chunk_lens if i]

    chunks = []
    curr_len = 0
    for i in chunk_lens:
        chunks.append(data[curr_len:curr_len+i])
        curr_len = curr_len+i
    return chunks


def pool_wrapper(func, args: list):
    if not args:
        return []

    if len(args) == 1:
        return [func(*args[0])]

    with multiprocessing.Pool() as pool:
        return pool.starmap(func, args)
