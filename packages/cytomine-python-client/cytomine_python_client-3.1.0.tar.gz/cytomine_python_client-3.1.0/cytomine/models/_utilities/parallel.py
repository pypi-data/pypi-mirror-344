# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2024. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

import errno
import os
import queue
from multiprocessing import cpu_count
from threading import Thread
from typing import Any, Callable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar("T")  # Type of elements in data
R = TypeVar("R")  # Return type of worker_fn


def is_false(v: Any) -> bool:
    """Check if v is 'False'"""
    return isinstance(v, bool) and not v


def generic_parallel(
    data: Iterable[T],
    worker_fn: Callable[[T], Optional[R]],
    n_workers: int = 0,
) -> List[Tuple[T, Optional[R]]]:
    """Run a function on a batch of data in parallel using a given processing function.

    Parameters
    ----------
    data: iterable
        The data to be downloaded with `download_instance_fn`
    worker_fn: callable
        A functions that execute the operation on the given output.
        It has one parameter which must be the same type
        as the items of `data`. If needed it can return a value.
    n_workers: int
        Number of workers to use (default: uses all the available processors)

    Returns
    -------
    results: iterable
        List processed items as tuples. First element of the tuple is the item itself,
        the second element of the tuple is the value returned by `worker_fn` for this item.
    """

    def worker(_in: Any, _out: Any) -> None:
        while True:
            item = _in.get()
            if item is None:
                break
            _out.put((item, worker_fn(item)))

    if n_workers <= 0:
        n_workers = cpu_count()

    # instantiate multiprocessing objects
    in_queue: queue.Queue = queue.Queue()
    out_queue: queue.Queue = queue.Queue()
    threads = [
        Thread(target=worker, args=[in_queue, out_queue]) for _ in range(n_workers)
    ]

    for t in threads:
        t.daemon = True
        t.start()

    for item in data:
        if item is None:
            continue
        in_queue.put(item)

    # feed `n_workers` None values in the queue to stop the workers
    for _ in range(n_workers):
        in_queue.put(None)

    # wait for the jobs to finish
    for t in threads:
        t.join()

    results = []
    while not out_queue.empty():
        results.append(out_queue.get_nowait())

    return results


def generic_chunk_parallel(
    data: List[T],
    worker_fn: Callable[[List[T]], R],
    chunk_size: int = 1,
    n_workers: int = 0,
) -> List[Tuple[Tuple[int, int], R]]:
    """Execute a worker function on all elements of a data list.
    Items are processed by batch of size 'chunk_size'.

    Parameters
    ---------
    data: iterable
        Data to be processed (data should be sliceable)
    worker_fn: callable
        A callable function that can process a batch of items from data
        (received as a list of items)
    chunk_size: int
        Size of the chunk
    n_workers: int
        Number of workers to use (default: uses all the available processors)

    Returns
    -------
    results: iterable
        List processed items as tuples. First element of the tuple is the slice
        (start,end) of the chunk (end excluded),
        the second element of the tuple is the value returned by `worker_fn` for this slice.
    """
    nb_chunks = (len(data) + chunk_size) // chunk_size
    chunk_limits = []

    for i in range(nb_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_limits.append([start, end])

    def worker_wrapper(startend: Tuple[int, int]) -> R:
        _start, _end = startend
        return worker_fn(data[_start:_end])

    return generic_parallel(chunk_limits, worker_wrapper, n_workers=n_workers)  # type: ignore


def generic_download(
    data: Iterable[T],
    download_instance_fn: Callable[[T], Optional[R]],
    n_workers: int = 0,
) -> List[Tuple[T, Optional[R]]]:
    """Download a set of data in parallel using a given download function.

    Parameters
    ----------
    data: iterable
        The data to be downloaded with `download_instance_fn`
    download_instance_fn: callable
        A functions that downloads what needs to be downloaded.
        It has one parameter which must be the same type as the
        items of `data`. If needed it can return a value.
    n_workers: int
        Number of workers to use (default: uses all the available processors)

    Returns
    -------
    results: iterable
        List processed items as tuples. First element of the tuple is the item itself,
        the second element of the tuple
        is the value returned by `download_instance_fn` for this item.
    """
    return generic_parallel(data, download_instance_fn, n_workers=n_workers)


def makedirs(path: str, exist_ok: bool = True) -> None:
    """Python 2.7 compatinle"""
    if path:
        try:
            os.makedirs(path)
        except OSError as e:
            if not (exist_ok and e.errno == errno.EEXIST):
                raise  # Reraise if failed for reasons other than existing already
